"""
Shoonya Wipe - Production Safety Controls

Safety controls and validations for production mode operations.
"""

import os
import subprocess
import logging
from typing import List, Tuple
from pathlib import Path

class SafetyController:
    """Controls safety measures for production operations."""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.safety_checks_enabled = True
    
    def validate_production_environment(self) -> Tuple[bool, List[str]]:
        """Validate that the environment is safe for production operations."""
        errors = []
        
        # Check if running as root
        if os.geteuid() != 0:
            errors.append("Production mode requires root privileges")
        
        # Check if production mode is enabled
        if not os.getenv("SHOONYA_PRODUCTION_MODE"):
            errors.append("Production mode not enabled. Set SHOONYA_PRODUCTION_MODE=1")
        
        # Check if safety checks are disabled
        if os.getenv("SHOONYA_DISABLE_SAFETY_CHECKS"):
            self.logger.warning("Safety checks are disabled - proceed with extreme caution")
            self.safety_checks_enabled = False
        
        return len(errors) == 0, errors
    
    def validate_device_safety(self, device_path: str) -> Tuple[bool, List[str]]:
        """Validate device for safe erasing."""
        if not self.safety_checks_enabled:
            return True, []
        
        errors = []
        
        # Check if device exists
        if not Path(device_path).exists():
            errors.append(f"Device {device_path} does not exist")
            return False, errors
        
        # Check if it's a real block device
        if not device_path.startswith('/dev/'):
            errors.append(f"Invalid device path: {device_path}")
            return False, errors
        
        # Check if device is mounted
        if self._is_device_mounted(device_path):
            errors.append(f"Device {device_path} is currently mounted")
        
        # Check if it's a system drive
        if self._is_system_drive(device_path):
            errors.append(f"Device {device_path} appears to be a system drive")
        
        # Check if it's a critical system device
        if self._is_critical_device(device_path):
            errors.append(f"Device {device_path} is a critical system device")
        
        return len(errors) == 0, errors
    
    def _is_device_mounted(self, device_path: str) -> bool:
        """Check if device is currently mounted."""
        try:
            result = subprocess.run(
                ['mount'], capture_output=True, text=True, check=True
            )
            return device_path in result.stdout
        except:
            return False
    
    def _is_system_drive(self, device_path: str) -> bool:
        """Check if device appears to be a system drive."""
        system_drives = ['/dev/sda', '/dev/nvme0n1', '/dev/mmcblk0']
        return any(device_path.startswith(drive) for drive in system_drives)
    
    def _is_critical_device(self, device_path: str) -> bool:
        """Check if device is critical for system operation."""
        critical_devices = [
            '/dev/sda1', '/dev/sda2',  # Common boot partitions
            '/dev/nvme0n1p1', '/dev/nvme0n1p2',  # NVMe boot partitions
            '/dev/mmcblk0p1', '/dev/mmcblk0p2',  # eMMC boot partitions
        ]
        return device_path in critical_devices
    
    def require_confirmation(self, device_path: str, method: str) -> bool:
        """Require user confirmation for destructive operations."""
        if not self.safety_checks_enabled:
            return True
        
        print(f"\n⚠️  WARNING: DESTRUCTIVE OPERATION ⚠️")
        print(f"Device: {device_path}")
        print(f"Method: {method}")
        print(f"This operation will PERMANENTLY ERASE all data on this device!")
        print(f"This action CANNOT be undone!")
        
        response = input("\nAre you absolutely sure you want to proceed? (type 'YES' to confirm): ")
        return response == "YES"
    
    def log_safety_event(self, event: str, device_path: str = None):
        """Log safety-related events."""
        message = f"SAFETY EVENT: {event}"
        if device_path:
            message += f" - Device: {device_path}"
        
        self.logger.warning(message)
        
        # Could also write to a dedicated safety log file
        # with open("/var/log/shoonya-safety.log", "a") as f:
        #     f.write(f"{datetime.now()}: {message}\n")

