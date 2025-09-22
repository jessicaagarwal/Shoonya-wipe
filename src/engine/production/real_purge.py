"""
Shoonya Wipe - Real Purge Engine

NIST Purge method implementation for real devices.
"""

import logging
from datetime import datetime
from ...core.shared.nist_types import DeviceInfo, SanitizationResult, SanitizationMethod, SanitizationTechnique
from ...core.production.real_device import RealDeviceWiper

class RealPurgeEngine:
    """Real device Purge method implementation."""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.wiper = RealDeviceWiper()
    
    def execute_purge(self, device: DeviceInfo) -> SanitizationResult:
        """Execute NIST Purge method on real device."""
        try:
            self.logger.info(f"Starting Purge method on {device.path}")
            
            # Execute real device wipe
            success, message = self.wiper.execute_purge(device.path)
            
            if success:
                # Verify the wipe
                verify_success, verify_message = self.wiper.verify_wipe(device.path)
                
                # Determine technique used
                technique = self._determine_technique(device)
                
                result = SanitizationResult(
                    success=success,
                    method=SanitizationMethod.PURGE,
                    technique=technique,
                    verification_status="passed" if verify_success else "failed",
                    completion_time=datetime.utcnow(),
                    verification_details=[
                        "Real device Purge method executed",
                        f"Device: {device.path}",
                        f"Method: {technique.value}",
                        f"Verification: {verify_message}"
                    ]
                )
                
                self.logger.info("Purge method completed successfully")
                return result
            else:
                result = SanitizationResult(
                    success=False,
                    method=SanitizationMethod.PURGE,
                    technique=SanitizationTechnique.SSD_SECURE_ERASE,
                    verification_status="failed",
                    error_message=message,
                    completion_time=datetime.utcnow(),
                    verification_details=[
                        "Real device Purge method failed",
                        f"Device: {device.path}",
                        f"Error: {message}"
                    ]
                )
                
                self.logger.error(f"Purge method failed: {message}")
                return result
                
        except Exception as e:
            error_msg = f"Unexpected error in Purge method: {e}"
            self.logger.error(error_msg)
            
            return SanitizationResult(
                success=False,
                method=SanitizationMethod.PURGE,
                technique=SanitizationTechnique.SSD_SECURE_ERASE,
                verification_status="failed",
                error_message=error_msg,
                completion_time=datetime.utcnow(),
                verification_details=[
                    "Real device Purge method failed with exception",
                    f"Device: {device.path}",
                    f"Error: {error_msg}"
                ]
            )
    
    def _determine_technique(self, device: DeviceInfo) -> SanitizationTechnique:
        """Determine the technique used based on device type."""
        if self.wiper._is_ssd_device(device.path):
            return SanitizationTechnique.SSD_SECURE_ERASE
        else:
            return SanitizationTechnique.SINGLE_PASS_OVERWRITE

