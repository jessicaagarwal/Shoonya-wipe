"""
Shoonya Wipe - Production Mode Manager

Handles production mode operations and safety controls for real device erasing.
"""

import os
import subprocess
import logging
from typing import Dict, List, Optional, Tuple
from pathlib import Path
from dataclasses import dataclass

@dataclass
class ProductionConfig:
    """Production mode configuration."""
    real_device_mode: bool = False
    require_root: bool = True
    safety_checks: bool = True
    backup_required: bool = True
    confirmation_required: bool = True
    log_level: str = "INFO"

class ProductionModeManager:
    """Manages production mode operations and safety controls."""
    
    def __init__(self):
        self.config = ProductionConfig()
        self.logger = logging.getLogger(__name__)
        self._setup_logging()
    
    def _setup_logging(self):
        """Setup logging for production mode."""
        logging.basicConfig(
            level=getattr(logging, self.config.log_level),
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
    
    def enable_production_mode(self) -> bool:
        """Enable production mode with safety checks."""
        try:
            # Check if running as root
            if self.config.require_root and os.geteuid() != 0:
                self.logger.error("Production mode requires root privileges")
                return False
            
            # Check for safety environment variable
            if not os.getenv("SHOONYA_PRODUCTION_MODE"):
                self.logger.error("Production mode not enabled. Set SHOONYA_PRODUCTION_MODE=1")
                return False
            
            self.config.real_device_mode = True
            self.logger.info("Production mode enabled - Real device erasing allowed")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to enable production mode: {e}")
            return False
    
    def is_production_mode(self) -> bool:
        """Check if production mode is enabled."""
        return (
            self.config.real_device_mode and
            os.getenv("SHOONYA_PRODUCTION_MODE") == "1"
        )
    
    def validate_device_for_production(self, device_path: str) -> Tuple[bool, str]:
        """Validate device for production erasing."""
        try:
            # Check if device exists
            if not Path(device_path).exists():
                return False, f"Device {device_path} does not exist"
            
            # Check if it's a real block device
            if not device_path.startswith('/dev/'):
                return False, f"Invalid device path: {device_path}"
            
            # Check if device is mounted
            if self._is_device_mounted(device_path):
                return False, f"Device {device_path} is currently mounted"
            
            # Check if it's a system drive
            if self._is_system_drive(device_path):
                return False, f"Device {device_path} appears to be a system drive"
            
            return True, "Device validation passed"
            
        except Exception as e:
            return False, f"Device validation failed: {e}"
    
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
    
    def get_real_device_wipe_commands(self, device_path: str, method: str) -> List[str]:
        """Get real device wipe commands based on method."""
        commands = []
        
        if method == "CLEAR":
            # Single pass overwrite
            commands.append(f"dd if=/dev/zero of={device_path} bs=1M status=progress")
            
        elif method == "PURGE":
            # Try SSD secure erase first
            if self._is_ssd_device(device_path):
                commands.append(f"hdparm --security-erase NULL {device_path}")
                commands.append(f"hdparm --security-erase-enhanced NULL {device_path}")
            else:
                # Fallback to overwrite
                commands.append(f"dd if=/dev/zero of={device_path} bs=1M status=progress")
        
        return commands
    
    def _is_ssd_device(self, device_path: str) -> bool:
        """Check if device is an SSD."""
        try:
            # Check if it's an NVMe device
            if device_path.startswith('/dev/nvme'):
                return True
            
            # Check if it's an ATA device with SSD characteristics
            result = subprocess.run(
                ['hdparm', '-I', device_path], 
                capture_output=True, text=True, check=True
            )
            return 'Solid State Device' in result.stdout
            
        except:
            return False
    
    def execute_real_wipe(self, device_path: str, method: str) -> Tuple[bool, str]:
        """Execute real device wipe with safety checks."""
        try:
            # Validate device
            is_valid, message = self.validate_device_for_production(device_path)
            if not is_valid:
                return False, message
            
            # Get wipe commands
            commands = self.get_real_device_wipe_commands(device_path, method)
            
            # Execute commands
            for cmd in commands:
                self.logger.info(f"Executing: {cmd}")
                result = subprocess.run(
                    cmd.split(), 
                    capture_output=True, 
                    text=True, 
                    check=True
                )
                self.logger.info(f"Command output: {result.stdout}")
            
            return True, "Real device wipe completed successfully"
            
        except subprocess.CalledProcessError as e:
            error_msg = f"Wipe command failed: {e.stderr}"
            self.logger.error(error_msg)
            return False, error_msg
        except Exception as e:
            error_msg = f"Unexpected error during wipe: {e}"
            self.logger.error(error_msg)
            return False, error_msg

# Global production mode manager
production_manager = ProductionModeManager()

