# aihpi - AI High Performance Infrastructure

A Python package for simplified distributed job submission on SLURM clusters with container support. Built on top of submitit with additional features specifically designed for AI/ML workloads.

## Features

- **Simple API**: Configure and submit jobs with minimal code
- **Distributed Training**: Automatic setup for multi-node distributed training
- **Container Support**: First-class support for Pyxis/Enroot containers
- **Remote Submission**: Submit jobs via SSH from remote machines
- **LlamaFactory Integration**: Built-in support for LlamaFactory training
- **Flexible Configuration**: Dataclass-based configuration system

## Installation

```bash
# Install from local directory
pip install -e .

# Or install with development dependencies
pip install -e ".[dev]"

# With HuggingFace integration
pip install -e ".[huggingface]"
```

## Quick Start

### Single-Node Job

```python
from aihpi import SlurmJobExecutor, JobConfig

# Configure the job
config = JobConfig(
    job_name="my-training",
    num_nodes=1,
    gpus_per_node=2,
    walltime="01:00:00",
    partition="aisc"
)

# Create executor and submit job
executor = SlurmJobExecutor(config)

def my_training():
    print("Running training...")
    # Your training code here
    return "Training completed"

job = executor.submit_function(my_training)
print(f"Job ID: {job.job_id}")
```

### Multi-Node Distributed Training

```python
from pathlib import Path
from aihpi import SlurmJobExecutor, JobConfig, ContainerConfig

# Configure multi-node job
config = JobConfig(
    job_name="distributed-training",
    num_nodes=4,
    gpus_per_node=2,
    walltime="04:00:00",
    partition="aisc",
    shared_storage_root=Path("/sc/home/username"),
)

# Configure container
config.container = ContainerConfig(
    name="torch2412",
    mounts=["/data:/workspace/data"]
)

executor = SlurmJobExecutor(config)

def distributed_training():
    import os
    print(f"Node rank: {os.getenv('NODE_RANK')}")
    print(f"World size: {os.getenv('WORLD_SIZE')}")
    # Your distributed training code here

job = executor.submit_distributed_training(distributed_training)
```

### LlamaFactory Training

```python
from aihpi import SlurmJobExecutor, JobConfig

config = JobConfig(
    job_name="llama-training",
    num_nodes=2,
    gpus_per_node=1,
    walltime="06:00:00",
    partition="aisc",
    workspace_mount=Path("/path/to/LLaMA-Factory"),
    setup_commands=["source /workspace/vnv/bin/activate"]
)

executor = SlurmJobExecutor(config)
job = executor.submit_llamafactory_training("examples/train_lora/llama3_lora_sft.yaml")
```

### Remote Job Submission

```python
from aihpi import SlurmJobExecutor, JobConfig

# Submit jobs from remote machine via SSH
config = JobConfig(
    job_name="remote-job",
    num_nodes=1,
    gpus_per_node=1,
    walltime="02:00:00", 
    partition="aisc",
    login_node="10.130.0.6"  # SSH to this login node
)

executor = SlurmJobExecutor(config)
job = executor.submit_function(my_training_function)
```

## Configuration Reference

### JobConfig

Main configuration class for SLURM jobs:

```python
@dataclass
class JobConfig:
    # Job identification
    job_name: str = "aihpi-job"
    
    # Resource allocation  
    num_nodes: int = 1
    gpus_per_node: int = 1
    cpus_per_task: int = 4
    walltime: str = "01:00:00"  # HH:MM:SS
    
    # SLURM configuration
    partition: str = "aisc"
    account: Optional[str] = None
    qos: Optional[str] = None
    
    # Paths and directories
    log_dir: Path = Path("logs/aihpi")
    shared_storage_root: Path = Path("/sc/home")
    workspace_mount: Optional[Path] = None
    
    # Container configuration
    container: ContainerConfig = ContainerConfig()
    
    # Environment
    hf_token_file: Path = Path.home() / ".huggingface" / "token"
    hf_home: Optional[Path] = None
    setup_commands: List[str] = []
    env_vars: dict = {}
    
    # SSH configuration
    login_node: Optional[str] = None
```

### ContainerConfig

Configuration for container-based jobs:

```python
@dataclass
class ContainerConfig:
    name: str = "torch2412"
    mount_home: bool = True
    workdir: str = "/workspace"
    writable: bool = True
    mounts: List[str] = []  # Additional mounts as "host:container" strings
```

## Environment Variables

The package automatically sets up these environment variables for distributed training:

- `MASTER_ADDR`: Address of the master node
- `MASTER_PORT`: Communication port (random 30000-50000)
- `NODE_RANK`: Rank of the current node (0 to num_nodes-1)
- `WORLD_SIZE`: Total number of processes
- `FORCE_TORCHRUN`: Set to "1" for LlamaFactory compatibility

## Examples

See `aihpi/examples.py` for complete working examples:

- Single-node job submission
- Multi-node distributed training
- LlamaFactory integration
- Remote submission via SSH
- Custom environment variables

## Requirements

- Python ≥ 3.8
- submitit ≥ 1.4.0
- Access to SLURM cluster with Pyxis/Enroot (for container jobs)

## License

MIT License - see LICENSE file for details.