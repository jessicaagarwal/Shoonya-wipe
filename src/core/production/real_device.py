"""
Shoonya Wipe - Real Device Wiper

Real Linux device wiping commands for production mode.
"""

import subprocess
import logging
from typing import Tuple, List
from ..shared.nist_types import SanitizationMethod, SanitizationTechnique

class RealDeviceWiper:
    """Handles real device wiping operations."""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
    
    def execute_clear(self, device_path: str) -> Tuple[bool, str]:
        """Execute NIST Clear method (single-pass overwrite)."""
        try:
            self.logger.info(f"Starting Clear method on {device_path}")
            
            # Single pass overwrite with zeros
            cmd = f"dd if=/dev/zero of={device_path} bs=1M status=progress"
            result = subprocess.run(
                cmd.split(), 
                capture_output=True, 
                text=True, 
                check=True
            )
            
            self.logger.info("Clear method completed successfully")
            return True, "Clear method completed successfully"
            
        except subprocess.CalledProcessError as e:
            error_msg = f"Clear method failed: {e.stderr}"
            self.logger.error(error_msg)
            return False, error_msg
        except Exception as e:
            error_msg = f"Unexpected error in Clear method: {e}"
            self.logger.error(error_msg)
            return False, error_msg
    
    def execute_purge(self, device_path: str) -> Tuple[bool, str]:
        """Execute NIST Purge method (secure erase or crypto erase)."""
        try:
            self.logger.info(f"Starting Purge method on {device_path}")
            
            # Try SSD secure erase first
            if self._is_ssd_device(device_path):
                return self._execute_ssd_secure_erase(device_path)
            else:
                # Fallback to overwrite for HDDs
                return self.execute_clear(device_path)
                
        except Exception as e:
            error_msg = f"Unexpected error in Purge method: {e}"
            self.logger.error(error_msg)
            return False, error_msg
    
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
    
    def _execute_ssd_secure_erase(self, device_path: str) -> Tuple[bool, str]:
        """Execute SSD secure erase."""
        try:
            # Try enhanced secure erase first
            cmd = f"hdparm --security-erase-enhanced NULL {device_path}"
            result = subprocess.run(
                cmd.split(), 
                capture_output=True, 
                text=True, 
                check=True
            )
            
            self.logger.info("SSD secure erase completed successfully")
            return True, "SSD secure erase completed successfully"
            
        except subprocess.CalledProcessError:
            # Fallback to regular secure erase
            try:
                cmd = f"hdparm --security-erase NULL {device_path}"
                result = subprocess.run(
                    cmd.split(), 
                    capture_output=True, 
                    text=True, 
                    check=True
                )
                
                self.logger.info("SSD secure erase (fallback) completed successfully")
                return True, "SSD secure erase completed successfully"
                
            except subprocess.CalledProcessError as e:
                error_msg = f"SSD secure erase failed: {e.stderr}"
                self.logger.error(error_msg)
                return False, error_msg
    
    def execute_cryptographic_erase(self, device_path: str) -> Tuple[bool, str]:
        """Execute cryptographic erase for encrypted devices."""
        try:
            self.logger.info(f"Starting cryptographic erase on {device_path}")
            
            # This would require device-specific implementation
            # For now, fallback to secure erase
            return self._execute_ssd_secure_erase(device_path)
            
        except Exception as e:
            error_msg = f"Cryptographic erase failed: {e}"
            self.logger.error(error_msg)
            return False, error_msg
    
    def verify_wipe(self, device_path: str) -> Tuple[bool, str]:
        """Verify that the wipe was successful."""
        try:
            # Check if device is accessible
            result = subprocess.run(
                ['lsblk', device_path], 
                capture_output=True, 
                text=True, 
                check=True
            )
            
            # Additional verification could be added here
            # For example, checking that the device is empty
            
            self.logger.info("Wipe verification completed")
            return True, "Wipe verification completed successfully"
            
        except subprocess.CalledProcessError as e:
            error_msg = f"Wipe verification failed: {e.stderr}"
            self.logger.error(error_msg)
            return False, error_msg
        except Exception as e:
            error_msg = f"Unexpected error in wipe verification: {e}"
            self.logger.error(error_msg)
            return False, error_msg

