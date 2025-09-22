"""
Shoonya Wipe - Real Dispatcher

Production mode dispatcher for real device operations.
"""

import logging
from ...core.shared.nist_types import DeviceInfo, SanitizationMethod
from ...core.production.production_mode import production_manager
from ...core.production.safety_controls import SafetyController
from .real_clear import RealClearEngine
from .real_purge import RealPurgeEngine

class RealDispatcher:
    """Dispatches real device operations based on NIST methods."""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.safety_controller = SafetyController()
        self.clear_engine = RealClearEngine()
        self.purge_engine = RealPurgeEngine()
    
    def execute_wipe(self, device: DeviceInfo, method: SanitizationMethod) -> bool:
        """Execute wipe operation on real device."""
        try:
            # Validate production environment
            env_valid, env_errors = self.safety_controller.validate_production_environment()
            if not env_valid:
                self.logger.error("Production environment validation failed:")
                for error in env_errors:
                    self.logger.error(f"  - {error}")
                return False
            
            # Validate device safety
            device_valid, device_errors = self.safety_controller.validate_device_safety(device.path)
            if not device_valid:
                self.logger.error("Device safety validation failed:")
                for error in device_errors:
                    self.logger.error(f"  - {error}")
                return False
            
            # Require confirmation
            if not self.safety_controller.require_confirmation(device.path, method.value):
                self.logger.warning("User cancelled operation")
                return False
            
            # Execute the appropriate method
            if method == SanitizationMethod.CLEAR:
                result = self.clear_engine.execute_clear(device)
            elif method == SanitizationMethod.PURGE:
                result = self.purge_engine.execute_purge(device)
            else:
                self.logger.error(f"Unsupported method: {method}")
                return False
            
            # Log the result
            if result.success:
                self.logger.info(f"Wipe operation completed successfully: {method.value}")
                self.safety_controller.log_safety_event("WIPE_COMPLETED", device.path)
            else:
                self.logger.error(f"Wipe operation failed: {result.error_message}")
                self.safety_controller.log_safety_event("WIPE_FAILED", device.path)
            
            return result.success
            
        except Exception as e:
            self.logger.error(f"Unexpected error in wipe execution: {e}")
            self.safety_controller.log_safety_event("WIPE_ERROR", device.path)
            return False
    
    def run_one_click_wipe(self, device: DeviceInfo) -> bool:
        """Run one-click wipe with automatic method selection."""
        try:
            # Determine best method for device
            method = self._determine_best_method(device)
            
            self.logger.info(f"One-click wipe: {method.value} on {device.path}")
            
            # Execute wipe
            return self.execute_wipe(device, method)
            
        except Exception as e:
            self.logger.error(f"One-click wipe failed: {e}")
            return False
    
    def _determine_best_method(self, device: DeviceInfo) -> SanitizationMethod:
        """Determine the best NIST method for the device."""
        # For production, prefer Purge for SSDs, Clear for HDDs
        if device.media_type == "Flash" or "ssd" in device.model.lower():
            return SanitizationMethod.PURGE
        else:
            return SanitizationMethod.CLEAR

