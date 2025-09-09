"""SLURM job executor with SSH and container support."""

import os
import random
import socket
import subprocess
import time
from pathlib import Path
from typing import Optional, Callable, Any
import shlex

import submitit
from submitit import JobEnvironment

from .config import JobConfig


def _shlex_join(argv):
    """Join arguments with proper shell escaping."""
    try:
        return shlex.join(argv)
    except AttributeError:
        # Fallback for Python < 3.8
        return " ".join(shlex.quote(a) for a in argv)


class SSHSlurmExecutor(submitit.SlurmExecutor):
    """SLURM executor that submits jobs via SSH."""
    
    def __init__(self, *args, login_node: str, **kwargs):
        super().__init__(*args, **kwargs)
        self._login_node = login_node
        self.ssh_base = [
            "ssh", "-q",
            "-o", "BatchMode=yes", 
            "-o", "StrictHostKeyChecking=no",
            "-o", "ConnectTimeout=10",
            login_node,
        ]
    
    def _make_submission_command(self, submission_file_path: str):
        """Wrap sbatch command with SSH."""
        sbatch_cmd = super()._make_submission_command(submission_file_path)
        return self.ssh_base + [_shlex_join(sbatch_cmd)]


class SlurmJobExecutor:
    """Main job executor class for distributed training."""
    
    def __init__(self, config: JobConfig):
        self.config = config
        self._executor = None
        
    def _get_executor(self):
        """Get the appropriate submitit executor."""
        if self._executor is None:
            if self.config.login_node:
                self._executor = SSHSlurmExecutor(
                    folder=self.config.log_dir,
                    login_node=self.config.login_node
                )
            else:
                self._executor = submitit.SlurmExecutor(folder=self.config.log_dir)
            
            # Configure executor parameters
            additional_params = {
                "constraint": "ARCH:X86",
                "export": self.config.get_export_string(),
            }
            
            # Add container parameters if using containers
            if self.config.container:
                additional_params.update({
                    "container_name": self.config.container.name,
                    "container_mount_home": self.config.container.mount_home,
                    "container_workdir": self.config.container.workdir,
                    "container_writable": self.config.container.writable,
                    "container_mounts": self.config.container.get_mount_string(),
                })
            
            self._executor.update_parameters(
                job_name=self.config.job_name,
                partition=self.config.partition,
                nodes=self.config.num_nodes,
                gpus_per_node=self.config.gpus_per_node,
                cpus_per_task=self.config.cpus_per_task,
                time=self.config.get_walltime_minutes(),
                use_srun=False,
                setup=self.config.setup_commands,
                additional_parameters=additional_params,
                account=self.config.account,
                qos=self.config.qos,
            )
            
        return self._executor
    
    def submit_function(self, func: Callable, *args, **kwargs) -> submitit.Job:
        """Submit a Python function as a job."""
        executor = self._get_executor()
        job = executor.submit(func, *args, **kwargs)
        
        print(f"🎉 Submitted SLURM job id: {job.job_id}")
        print(f"  Stdout will appear in:  {job.paths.stdout}")
        print(f"  Stderr will appear in:  {job.paths.stderr}")
        
        return job
    
    def submit_distributed_training(
        self, 
        training_function: Callable,
        config_path: Optional[str] = None,
        **kwargs
    ) -> submitit.Job:
        """
        Submit a distributed training job.
        
        Args:
            training_function: Function to run on each node
            config_path: Path to training configuration file
            **kwargs: Additional arguments to pass to training function
        """
        def distributed_wrapper():
            return self._distributed_training_wrapper(
                training_function, 
                config_path, 
                **kwargs
            )
        
        return self.submit_function(distributed_wrapper)
    
    def _distributed_training_wrapper(
        self, 
        training_function: Callable,
        config_path: Optional[str] = None,
        **kwargs
    ):
        """Wrapper function that sets up distributed training environment."""
        env = JobEnvironment()
        master_addr = env.hostnames[0]
        node_rank = env.node
        world_size = env.num_tasks
        
        # Set up distributed environment variables
        os.environ["MASTER_ADDR"] = master_addr
        os.environ["NODE_RANK"] = str(node_rank)
        os.environ["RANK"] = str(node_rank)
        os.environ["WORLD_SIZE"] = str(world_size)
        os.environ["FORCE_TORCHRUN"] = "1"
        
        # Set master port
        master_port = os.getenv("MASTER_PORT")
        if master_port is None:
            master_port = str(random.randint(30000, 50000))
            os.environ["MASTER_PORT"] = master_port
        
        if config_path:
            os.environ["CONFIG_PATH"] = config_path
        
        # Handle HuggingFace authentication on rank 0
        if node_rank == 0:
            self._setup_huggingface_auth()
        
        # Workers wait for master to be ready
        if node_rank != 0:
            self._wait_for_master(master_addr, int(master_port))
        
        # Run the actual training function
        return training_function(**kwargs)
    
    def _setup_huggingface_auth(self):
        """Set up HuggingFace authentication."""
        token = os.getenv("HUGGING_FACE_HUB_TOKEN")
        if token is None and self.config.hf_token_file.exists():
            token = self.config.hf_token_file.read_text().strip()
        
        if token:
            subprocess.run(
                ["huggingface-cli", "login", "--token", token],
                check=True,
            )
    
    def _wait_for_master(self, master_addr: str, master_port: int):
        """Wait for master node to be ready."""
        while True:
            try:
                s = socket.socket()
                s.connect((master_addr, master_port))
                s.close()
                break
            except OSError:
                time.sleep(1)
    
    def submit_llamafactory_training(self, config_path: str) -> submitit.Job:
        """
        Submit a LlamaFactory training job.
        
        Args:
            config_path: Path to LlamaFactory configuration YAML file
        """
        def llamafactory_train():
            cmd = [
                "llamafactory-cli", 
                "train",
                os.getenv("CONFIG_PATH", config_path),
            ]
            
            print(f"[{socket.gethostname()}|rank {os.getenv('NODE_RANK', 0)}] "
                  f"Launching: {' '.join(cmd)}", flush=True)
            
            subprocess.run(cmd, check=True)
        
        return self.submit_distributed_training(llamafactory_train, config_path)