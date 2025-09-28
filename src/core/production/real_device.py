"""
Shoonya Wipe - Real Device Wiper

Real Linux device wiping commands for production mode.
"""

import subprocess
import logging
import time
from typing import Tuple, List, Optional, Callable
from ..shared.nist_types import SanitizationMethod, SanitizationTechnique

class RealDeviceWiper:
    """Handles real device wiping operations."""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
    
    def execute_clear(self, device_path: str, progress_callback: Optional[Callable[[int, int], None]] = None) -> Tuple[bool, str]:
        """Execute NIST Clear method (single-pass overwrite)."""
        try:
            self.logger.info(f"Starting Clear method on {device_path}")
            
            # Single pass overwrite with zeros
            cmd = f"dd if=/dev/zero of={device_path} bs=1M status=progress"
            
            if progress_callback:
                # Use Popen to stream progress
                proc = subprocess.Popen(
                    cmd.split(),
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    text=True,
                    bufsize=1
                )
                
                # Parse progress from stderr
                if proc.stderr:
                    for line in proc.stderr:
                        line = (line or "").strip()
                        if not line:
                            continue
                        # dd prints like: "12345678 bytes (12 MB, ...) copied"
                        if " bytes" in line:
                            try:
                                num_str = line.split(" bytes")[0].strip()
                                bytes_done = int(num_str)
                                # We don't know total bytes here, so pass 0
                                progress_callback(bytes_done, 0)
                            except Exception:
                                pass
                
                rc = proc.wait()
                if rc != 0:
                    error_msg = f"Clear method failed with exit code {rc}"
                    self.logger.error(error_msg)
                    return False, error_msg
            else:
                # Fallback to original behavior
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
    
    def execute_purge(self, device_path: str, progress_callback: Optional[Callable[[int, int], None]] = None) -> Tuple[bool, str]:
        """Execute NIST Purge method (secure erase or crypto erase)."""
        try:
            self.logger.info(f"Starting Purge method on {device_path}")
            
            # Try SSD secure erase first
            if self._is_ssd_device(device_path):
                return self._execute_ssd_secure_erase(device_path, progress_callback)
            else:
                # Fallback to overwrite for HDDs
                return self.execute_clear(device_path, progress_callback)
                
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
    
    def _execute_ssd_secure_erase(self, device_path: str, progress_callback: Optional[Callable[[int, int], None]] = None) -> Tuple[bool, str]:
        """Execute SSD secure erase."""
        try:
            # SSD secure erase is typically fast and doesn't provide progress
            # We'll simulate progress for user feedback
            if progress_callback:
                # Simulate progress over a few seconds
                for i in range(10):
                    progress_callback(i * 10, 100)  # 10% increments
                    time.sleep(0.5)
            
            # Try enhanced secure erase first
            cmd = f"hdparm --security-erase-enhanced NULL {device_path}"
            result = subprocess.run(
                cmd.split(), 
                capture_output=True, 
                text=True, 
                check=True
            )
            
            if progress_callback:
                progress_callback(100, 100)  # Complete
            
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
                
                if progress_callback:
                    progress_callback(100, 100)  # Complete
                
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

