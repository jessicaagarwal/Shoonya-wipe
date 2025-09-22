"""
Shoonya Wipe - Real Clear Engine

NIST Clear method implementation for real devices.
"""

import logging
from datetime import datetime
from core.shared.nist_types import DeviceInfo, SanitizationResult, SanitizationMethod, SanitizationTechnique
from core.production.real_device import RealDeviceWiper

class RealClearEngine:
    """Real device Clear method implementation."""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.wiper = RealDeviceWiper()
    
    def execute_clear(self, device: DeviceInfo) -> SanitizationResult:
        """Execute NIST Clear method on real device."""
        try:
            self.logger.info(f"Starting Clear method on {device.path}")
            
            # Execute real device wipe
            success, message = self.wiper.execute_clear(device.path)
            
            if success:
                # Verify the wipe
                verify_success, verify_message = self.wiper.verify_wipe(device.path)
                
                result = SanitizationResult(
                    success=success,
                    method=SanitizationMethod.CLEAR,
                    technique=SanitizationTechnique.SINGLE_PASS_OVERWRITE,
                    verification_status="passed" if verify_success else "failed",
                    completion_time=datetime.utcnow(),
                    verification_details=[
                        "Real device Clear method executed",
                        f"Device: {device.path}",
                        f"Method: Single Pass Overwrite",
                        f"Verification: {verify_message}"
                    ]
                )
                
                self.logger.info("Clear method completed successfully")
                return result
            else:
                result = SanitizationResult(
                    success=False,
                    method=SanitizationMethod.CLEAR,
                    technique=SanitizationTechnique.SINGLE_PASS_OVERWRITE,
                    verification_status="failed",
                    error_message=message,
                    completion_time=datetime.utcnow(),
                    verification_details=[
                        "Real device Clear method failed",
                        f"Device: {device.path}",
                        f"Error: {message}"
                    ]
                )
                
                self.logger.error(f"Clear method failed: {message}")
                return result
                
        except Exception as e:
            error_msg = f"Unexpected error in Clear method: {e}"
            self.logger.error(error_msg)
            
            return SanitizationResult(
                success=False,
                method=SanitizationMethod.CLEAR,
                technique=SanitizationTechnique.SINGLE_PASS_OVERWRITE,
                verification_status="failed",
                error_message=error_msg,
                completion_time=datetime.utcnow(),
                verification_details=[
                    "Real device Clear method failed with exception",
                    f"Device: {device.path}",
                    f"Error: {error_msg}"
                ]
            )

