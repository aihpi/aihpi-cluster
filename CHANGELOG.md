# Change Log
All notable changes to this project will be documented in this file.
 
The format is based on [Keep a Changelog](http://keepachangelog.com/)
and this project adheres to [Semantic Versioning](http://semver.org/).
 
## [Unreleased] - yyyy-mm-dd
 
### Added
- Nothing yet.

### Changed
- Nothing yet.

### Fixed
- Nothing yet.

## [0.1.2] - 2025-09-10

### Added
- **CLI Interface**: New `aihpi` command-line tool for job submission and management
  - `aihpi run` - Submit jobs with automatic mode detection (function/distributed/CLI)
  - `aihpi monitor` - Monitor job status with real-time updates
  - `aihpi status` - List all user jobs
  - `aihpi cancel` - Cancel running jobs
  - `aihpi logs` - View job logs (placeholder for future implementation)
- **Automatic Submission Mode Detection**: CLI automatically chooses appropriate submission method based on configuration and command type
- **Colored Terminal Output**: Enhanced user experience with colored status messages and job information
- **Config Validation**: Comprehensive validation for JobConfig parameters with detailed error messages
- **Installation Guides**: Added collapsible dropdown installation instructions for both pip and UV package managers
- **Test Framework**: Added pytest configuration and test structure in `tests/` directory
- **Package Configuration**: Added comprehensive `pyproject.toml` with build system, dependencies, and development tools
- **Example Configurations**: Added example config files in `aihpi/examples/configs/` directory
- **Training Examples**: Added `train_example.py` with practical training job examples
- **UV Lock File**: Added `uv.lock` for reproducible dependency management

### Changed
- **Refactored Examples**: Updated executor examples to use `submit_cli_training` consistently
- **Enhanced README**: Added comprehensive CLI usage examples and configuration documentation
- **Installation Documentation**: Restructured installation section with dropdown sections for pip and UV

## [0.1.1] - 2025-09-09

Bug fixes and improvements for stable job submission and log organization.

### Added
- Job-specific log directories with timestamp-based naming
- Abstracted CLI training submission method (`submit_cli_training`)
- Clean job folder organization without interfering with submitit paths
- Comprehensive error handling for job submission failures
- Better job directory management and cleanup

### Changed
- Updated all examples to include `login_node` configuration parameter
- Improved README with `login_node` setup instructions and requirements
- Enhanced distributed training configuration with `ntasks_per_node=1`
- Simplified job submission flow without folder renaming
- Updated CLAUDE.md with development commands and architecture overview

### Fixed
- **BREAKING**: Fixed missing `JobPaths` import in monitoring module (was `submitit.JobPaths`, now correctly imports from `submitit.core.utils.JobPaths`)
- Fixed container mount configuration issues in multi-node example
- Fixed multi-node distributed training by adding proper SLURM task configuration
- Fixed job log path consistency issues that caused "could not find submitted jobs" errors
- Fixed temporary folder cleanup and orphaned directory issues
- Corrected container mount syntax in examples (host_path:container_path format)

## [0.1.0] - 2025-09-09
  
Initial release of aihpi package for SLURM job submission.

### Added
- Core job submission functionality with SlurmJobExecutor
- Support for single-node and multi-node distributed training
- Container support with Pyxis/Enroot integration
- SSH remote job submission capabilities
- Real-time job monitoring and log streaming with JobMonitor
- Experiment tracking integrations:
  - Weights & Biases (wandb) support
  - MLflow integration  
  - Local file-based tracking
- Comprehensive configuration system with JobConfig and ContainerConfig
- Built-in LlamaFactory training support
- Complete examples and documentation
- Organized package structure with core, monitoring, tracking, and examples modules

### Changed
- Updated README with comprehensive aihpi documentation
- Modified template structure to accommodate Python package

### Fixed
- N/A (initial release)