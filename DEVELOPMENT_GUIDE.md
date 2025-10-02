# Shoonya Wipe Development Guide

## Overview

This guide covers the development setup, architecture, and contribution guidelines for Shoonya Wipe.

## Architecture

### Core Components

#### 1. **NIST Compliance Engine** (`src/core/nist_compliance.py`)
- Implements NIST SP 800-88r2 guidelines
- AI decision flowchart for method selection
- Verification and validation logic
- Certificate generation with all required fields

#### 2. **Modular Wipe Engine** (`src/core/engine/`)
- **`clear.py`** - NIST Clear method (single-pass overwrite)
- **`purge.py`** - NIST Purge method (secure erase, crypto erase)
- **`certificate.py`** - NIST-compliant certificate generation
- **`utils.py`** - Device detection and utility functions
- **`dispatcher.py`** - Engine coordination and one-click mode

#### 3. **Web Interface** (`src/web/web_gui.py`)
- Flask-based web application
- Real-time progress tracking
- Device detection and selection
- File generation and download

#### 4. **CLI Interface** (`src/core/safeerase.py`)
- Rich console interface
- Interactive device selection
- NIST compliance workflow
- Certificate generation

#### 5. **Sandbox Environment** (`src/core/sandbox.py`)
- Safe testing with virtual media
- Simulated wipe operations
- File-based virtual disks

## Development Setup

### Prerequisites
- Python 3.11+
- Docker and Docker Compose
- Git

### Local Development

1. **Clone the repository**
```bash
git clone https://github.com/jessicaagarwal/shoonya-wipe.git
cd shoonya-wipe
```

2. **Set up Python environment**
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# or
venv\Scripts\activate     # Windows

pip install -r requirements.txt
```

3. **Run tests**
```bash
# Web interface
python main.py web

# CLI interface
python main.py cli

# One-click engine
python main.py engine
```

### Docker Development

1. **Start development environment**
```bash
docker compose up -d
```

2. **Access the application**
- Web interface: http://localhost:5000
- Container shell: `docker compose exec shoonya-wipe-web bash`

3. **View logs**
```bash
docker logs shoonya-wipe-web -f
```

## Code Structure

### Key Files

#### `main.py`
Entry point that dispatches to different interfaces:
- `web` - Web GUI
- `cli` - Command-line interface
- `verify` - Certificate verification
- `engine` - One-click wipe engine

#### `src/core/nist_compliance.py`
Core NIST compliance logic:
- `NISTComplianceEngine` class
- Decision flowchart implementation
- Method validation and selection
- Certificate generation

#### `src/web/web_gui.py`
Flask web application:
- Device detection API
- Wipe process management
- File generation and serving
- Real-time status updates

#### `src/core/engine/`
Modular wipe engine:
- Separate implementations for Clear/Purge methods
- Utility functions for device detection
- Certificate generation
- Engine dispatcher for one-click mode

### Data Flow

1. **Device Detection**
   - Cross-platform device scanning
   - Virtual media support
   - Device information extraction

2. **Method Selection**
   - NIST decision flowchart
   - Device type analysis
   - Method validation

3. **Wipe Execution**
   - Progress simulation
   - Sandbox operations
   - Real-time status updates

4. **Verification & Certification**
   - NIST compliance verification
   - Digital certificate generation
   - File signing and validation

## Testing

### Virtual Media Testing
- Uses 2GB virtual disk images (`virtual_media/vdisk*.img`)
- Safe testing without real drive access
- Full functionality testing

### Test Scenarios
1. **Device Detection** - Verify all devices are detected
2. **Method Selection** - Test NIST decision flowchart
3. **Wipe Process** - Test progress simulation and completion
4. **Certificate Generation** - Verify PDF and JSON generation
5. **File Download** - Test file serving and download

### Running Tests
```bash
# Start Docker environment
docker compose up -d

# Access web interface
open http://localhost:5000

# Test wipe process
curl -X POST http://localhost:5000/api/wipe \
  -H "Content-Type: application/json" \
  -d '{"device": "/app/virtual_media/vdisk0.img", "operator_name": "Test User", "operator_title": "Admin", "will_reuse": true, "sensitivity": "medium", "leaves_control": false}'
```

## Configuration

### Environment Variables
- `SAFEERASE_MODE` - Operation mode (web/cli/engine)
- `SAFEERASE_DEBUG` - Debug mode flag
- `SAFEERASE_OUTPUT_DIR` - Output directory for certificates

### Docker Configuration
- `docker-compose.yml` - Service configuration
- `Dockerfile` - Container image definition
- Volume mounts for persistent data

## Contributing

### Code Style
- Follow PEP 8 Python style guide
- Use type hints where appropriate
- Document functions and classes
- Add docstrings for public APIs

### Pull Request Process
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Update documentation
6. Submit a pull request

### Commit Messages
Use conventional commit format:
```
feat: add new feature
fix: fix bug
docs: update documentation
test: add tests
refactor: refactor code
```

## Troubleshooting

### Common Issues

#### 1. **Docker Container Won't Start**
```bash
# Check Docker status
docker ps -a

# View container logs
docker logs safeerase-pro-web

# Rebuild container
docker compose up --build -d
```

#### 2. **Web Interface Not Accessible**
- Check if port 5000 is available
- Verify Docker container is running
- Check firewall settings

#### 3. **Device Detection Issues**
- Ensure virtual media files exist
- Check file permissions
- Verify device detection logic

#### 4. **Certificate Generation Fails**
- Check if `out/` directory exists
- Verify file permissions
- Check for missing dependencies

### Debug Mode
```bash
# Enable debug logging
export SAFEERASE_DEBUG=1
python main.py web
```

## Security Considerations

### Development Security
- Never test on real drives
- Use virtual media for all testing
- Verify Docker container isolation
- Check file permissions and access

### Production Deployment
- Add authentication if needed
- Use HTTPS in production
- Implement proper logging
- Regular security updates

## Performance

### Optimization Areas
- Device detection speed
- Progress simulation timing
- File generation efficiency
- Memory usage optimization

### Monitoring
- Container resource usage
- API response times
- File generation performance
- Error rates and logging

## Future Enhancements

### Planned Features
- Real device support (with safety controls)
- Additional NIST methods
- Enhanced certificate templates
- Batch processing capabilities
- Advanced verification tools

### Technical Debt
- Code refactoring and cleanup
- Enhanced error handling
- Improved logging and monitoring
- Performance optimizations
