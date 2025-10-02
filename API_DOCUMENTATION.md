# Shoonya Wipe API Documentation

## Overview

Shoonya Wipe provides both a web API and CLI interface for secure data wiping with NIST SP 800-88r2 compliance. This document covers the API endpoints, data structures, and usage examples.

## Web API Endpoints

### Base URL
```
http://localhost:5000
```

### 1. Get Available Devices
**GET** `/api/devices`

Returns a list of available storage devices for wiping.

**Response:**
```json
[
  {
    "name": "VDISK0",
    "path": "/app/virtual_media/vdisk0.img",
    "model": "Sandbox VDisk",
    "serial": "SBX-vdisk0",
    "size": "2G",
    "transport": "file",
    "media_type": "Magnetic",
    "is_encrypted": false,
    "encryption_always_on": false
  }
]
```

### 2. Start Wipe Process
**POST** `/api/wipe`

Initiates a NIST-compliant wipe process on the specified device.

**Request Body:**
```json
{
  "device": "/app/virtual_media/vdisk0.img",
  "operator_name": "John Doe",
  "operator_title": "Security Admin",
  "will_reuse": true,
  "sensitivity": "medium",
  "leaves_control": false
}
```

**Response:**
```json
{
  "message": "NIST-compliant wipe started",
  "will_reuse": true,
  "sensitivity": "medium",
  "leaves_control": false
}
```

### 3. Get Wipe Status
**GET** `/api/status`

Returns the current status of the wipe process.

**Response:**
```json
{
  "completed": true,
  "compliance_checked": true,
  "current_pass": 1,
  "files": [
    "/app/out/wipelog.json",
    "/app/out/wipelog_signed.json",
    "/app/out/nist_certificate.pdf"
  ],
  "nist_method": "Clear",
  "nist_technique": "Single Pass Overwrite",
  "output": "Artifacts generated successfully",
  "progress": 100,
  "running": false,
  "status_message": "Sanitization complete!",
  "throughput": "0 MB/s",
  "time_remaining": "Calculating...",
  "total_passes": 1,
  "validation_warnings": [],
  "verification_status": "passed"
}
```

### 4. Download Generated Files
**GET** `/download?path=<file_path>`

Downloads generated certificates and logs.

**Example:**
```
GET /download?path=/app/out/nist_certificate.pdf
```

### 5. Verify Certificate
**GET** `/api/verify`

Verifies the digital signature of generated certificates.

**Response:**
```json
{
  "verified": true,
  "message": "Certificate verification successful"
}
```

## Data Structures

### Device Information
```python
class DeviceInfo:
    name: str                    # Device name (e.g., "VDISK0")
    path: str                    # Device path (e.g., "/app/virtual_media/vdisk0.img")
    model: str                   # Device model (e.g., "Sandbox VDisk")
    serial: str                  # Serial number (e.g., "SBX-vdisk0")
    size: str                    # Device size (e.g., "2G")
    transport: str               # Transport type (e.g., "file", "nvme", "sata")
    media_type: str              # Media type (e.g., "Magnetic", "Flash")
    is_encrypted: bool           # Encryption status
    encryption_always_on: bool   # Always-on encryption status
```

### NIST Compliance Methods
```python
class SanitizationMethod(Enum):
    CLEAR = "Clear"              # Single-pass overwrite
    PURGE = "Purge"              # Secure erase/crypto erase
    DESTROY = "Destroy"          # Physical destruction (guidance only)

class SanitizationTechnique(Enum):
    SINGLE_PASS_OVERWRITE = "Single Pass Overwrite"
    SSD_SECURE_ERASE = "SSD Secure Erase"
    CRYPTOGRAPHIC_ERASE = "Cryptographic Erase"
```

### Certificate Structure
```json
{
  "manufacturer": "Sandbox",
  "model": "Virtual Disk",
  "serial_number": "VDISK-0",
  "media_type": "Virtual",
  "sanitization_method": "Clear",
  "sanitization_technique": "Single Pass Overwrite",
  "tool_used": "Shoonya Wipe v1.0",
  "verification_method": "Web mode verification",
  "operator_name": "Web Operator",
  "operator_title": "User",
  "date": "2025-09-21T19:47:18.123456Z",
  "device_path": "/app/virtual_media/vdisk0.img",
  "device_size": "2G",
  "verification_status": "passed",
  "verification_details": ["Web mode verification completed"],
  "completion_time": "2025-09-21T19:47:18.123456Z",
  "certificate_id": "uuid-string",
  "nist_compliance": "SP 800-88r2"
}
```

## CLI Interface

### Main Commands
```bash
# Web interface
python main.py web

# CLI interface
python main.py cli

# Verification tool
python main.py verify

# One-click wipe engine
python main.py engine
```

### CLI Usage Examples
```bash
# Interactive CLI
python main.py cli

# One-click wipe (automatic method selection)
python main.py engine

# Verify a certificate
python main.py verify --file certificate.json
```

## Error Handling

### Common Error Responses
```json
{
  "error": "Device not found",
  "message": "The specified device path does not exist"
}
```

```json
{
  "error": "Wipe in progress",
  "message": "Another wipe operation is already running"
}
```

```json
{
  "error": "Invalid device",
  "message": "Device is not suitable for wiping"
}
```

## Security Considerations

1. **Docker Sandboxing** - All operations run in isolated containers
2. **Virtual Media** - Uses virtual disk images for safe testing
3. **Digital Signatures** - All certificates are cryptographically signed
4. **NIST Compliance** - Follows NIST SP 800-88r2 guidelines
5. **Audit Trail** - Complete logging of all operations

## Rate Limiting

- No rate limiting currently implemented
- Single wipe operation at a time
- Concurrent requests are queued

## Authentication

- No authentication required for local usage
- Designed for trusted network environments
- Consider adding authentication for production deployments
