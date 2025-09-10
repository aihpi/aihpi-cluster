"""Test configuration and fixtures for aihpi tests."""

import pytest
from pathlib import Path
from unittest.mock import Mock
import submitit

from aihpi.core.config import JobConfig, ContainerConfig


@pytest.fixture
def basic_job_config():
    """Basic job configuration for testing."""
    return JobConfig(
        job_name="test-job",
        num_nodes=1,
        gpus_per_node=1,
        walltime="00:30:00",
        partition="test",
        login_node="test.cluster.com",
    )


@pytest.fixture
def multi_node_job_config():
    """Multi-node job configuration for testing."""
    return JobConfig(
        job_name="test-multi-node",
        num_nodes=2,
        gpus_per_node=2,
        walltime="01:00:00",
        partition="test",
        login_node="test.cluster.com",
        shared_storage_root=Path("/test/shared"),
    )


@pytest.fixture
def container_job_config():
    """Job configuration with container settings."""
    config = JobConfig(
        job_name="test-container-job",
        num_nodes=1,
        gpus_per_node=1,
        walltime="00:30:00",
        partition="test",
        login_node="test.cluster.com",
        workspace_mount=Path("/test/workspace"),
        setup_commands=["echo 'setup complete'"],
    )
    config.container = ContainerConfig(name="test-container")
    config.container.mounts.append("/test/workspace:/workspace")
    return config


@pytest.fixture
def mock_submitit_job():
    """Mock submitit Job object."""
    job = Mock(spec=submitit.Job)
    job.job_id = "12345"
    job.state = "PENDING"
    job.result.return_value = "Test completed"
    return job


@pytest.fixture
def mock_slurm_executor():
    """Mock SlurmExecutor."""
    executor = Mock()
    executor.update_parameters = Mock()
    executor.submit = Mock()
    return executor


@pytest.fixture
def mock_ssh_slurm_executor():
    """Mock SSHSlurmExecutor."""
    executor = Mock()
    executor.update_parameters = Mock()
    executor.submit = Mock()
    return executor


@pytest.fixture
def sample_training_function():
    """Sample training function for testing."""
    def training_func():
        return "Training completed successfully"
    return training_func


@pytest.fixture
def sample_distributed_function():
    """Sample distributed training function for testing."""
    def distributed_func():
        import os
        return f"Distributed training on node {os.getenv('NODE_RANK', '0')}"
    return distributed_func