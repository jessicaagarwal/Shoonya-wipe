"""
Shoonya Wipe - NIST Types and Data Structures

Common data types used across safe and production modes.
"""

from enum import Enum
from dataclasses import dataclass
from typing import Optional, List
from datetime import datetime

class SanitizationMethod(Enum):
    """NIST SP 800-88r2 sanitization methods."""
    CLEAR = "Clear"
    PURGE = "Purge"
    DESTROY = "Destroy"

class SanitizationTechnique(Enum):
    """NIST SP 800-88r2 sanitization techniques."""
    SINGLE_PASS_OVERWRITE = "Single Pass Overwrite"
    MULTI_PASS_OVERWRITE = "Multi Pass Overwrite"
    SSD_SECURE_ERASE = "SSD Secure Erase"
    CRYPTOGRAPHIC_ERASE = "Cryptographic Erase"
    PHYSICAL_DESTRUCTION = "Physical Destruction"

@dataclass
class DeviceInfo:
    """Device information structure."""
    name: str
    path: str
    model: Optional[str] = None
    serial: Optional[str] = None
    size: Optional[str] = None
    transport: Optional[str] = None
    media_type: Optional[str] = None
    is_encrypted: bool = False
    encryption_always_on: bool = False

@dataclass
class SanitizationResult:
    """Result of sanitization operation."""
    success: bool
    method: SanitizationMethod
    technique: SanitizationTechnique
    verification_status: str
    error_message: Optional[str] = None
    completion_time: Optional[datetime] = None
    verification_details: Optional[List[str]] = None

