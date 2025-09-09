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