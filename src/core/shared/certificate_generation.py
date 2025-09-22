"""
Shoonya Wipe - Certificate Generation

Common certificate generation utilities for both safe and production modes.
"""

import json
import uuid
from datetime import datetime
from typing import Dict, Any
from .nist_types import DeviceInfo, SanitizationResult

class CertificateGenerator:
    """Generate NIST-compliant certificates."""
    
    def generate_log(self, device: DeviceInfo, result: SanitizationResult, 
                    operator_name: str, operator_title: str) -> Dict[str, Any]:
        """Generate wipe log with NIST compliance data."""
        return {
            "device": {
                "path": device.path,
                "name": device.name,
                "model": device.model or "Unknown",
                "serial": device.serial or "Unknown",
                "size": device.size or "Unknown",
                "media_type": device.media_type or "Unknown",
            },
            "method": result.method.value,
            "technique": result.technique.value,
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "status": "completed" if result.success else "failed",
            "verification": result.verification_status,
            "nist_compliance": {
                "standard": "NIST SP 800-88r2",
                "method": result.method.value,
                "technique": result.technique.value,
                "verification_status": result.verification_status,
                "verification_details": result.verification_details or []
            },
            "operator": {
                "name": operator_name,
                "title": operator_title
            },
            "tool": {
                "name": "Shoonya Wipe",
                "version": "1.0"
            }
        }
    
    def generate_certificate(self, device: DeviceInfo, result: SanitizationResult,
                           operator_name: str, operator_title: str) -> Dict[str, Any]:
        """Generate NIST-compliant certificate."""
        return {
            "manufacturer": device.model or "Unknown",
            "model": device.model or "Unknown",
            "serial_number": device.serial or f"UNKNOWN-{device.name}",
            "media_type": device.media_type or "Unknown",
            "sanitization_method": result.method.value,
            "sanitization_technique": result.technique.value,
            "tool_used": "Shoonya Wipe v1.0",
            "verification_method": "NIST SP 800-88r2 compliance",
            "operator_name": operator_name,
            "operator_title": operator_title,
            "date": datetime.utcnow().isoformat() + "Z",
            "device_path": device.path,
            "device_size": device.size or "Unknown",
            "verification_status": result.verification_status,
            "verification_details": result.verification_details or [],
            "completion_time": result.completion_time.isoformat() + "Z" if result.completion_time else None,
            "certificate_id": str(uuid.uuid4()),
            "nist_compliance": "SP 800-88r2",
        }

