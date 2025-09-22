"""
Shoonya Wipe - Device Detection

Cross-platform device detection for both safe and production modes.
"""

import os
import subprocess
import platform
from typing import List, Dict, Optional
from .nist_types import DeviceInfo

class DeviceDetector:
    """Cross-platform device detection."""
    
    def __init__(self):
        self.system = platform.system().lower()
    
    def detect_devices(self) -> List[DeviceInfo]:
        """Detect available storage devices."""
        if self.system == "linux":
            return self._detect_linux_devices()
        elif self.system == "windows":
            return self._detect_windows_devices()
        else:
            return self._detect_virtual_devices()
    
    def _detect_linux_devices(self) -> List[DeviceInfo]:
        """Detect devices on Linux systems."""
        devices = []
        
        try:
            # Use lsblk to get device information
            result = subprocess.run(
                ['lsblk', '-J'], 
                capture_output=True, text=True, check=True
            )
            
            import json
            data = json.loads(result.stdout)
            
            for device in data.get('blockdevices', []):
                if device.get('type') == 'disk':
                    device_info = DeviceInfo(
                        name=device.get('name', ''),
                        path=f"/dev/{device.get('name', '')}",
                        model=device.get('model', ''),
                        serial=device.get('serial', ''),
                        size=device.get('size', ''),
                        transport=device.get('tran', ''),
                        media_type=self._get_media_type(device),
                        is_encrypted=False,  # Would need additional checks
                        encryption_always_on=False
                    )
                    devices.append(device_info)
                    
        except Exception as e:
            print(f"Error detecting Linux devices: {e}")
            # Fallback to virtual devices for safety
            return self._detect_virtual_devices()
        
        return devices
    
    def _detect_windows_devices(self) -> List[DeviceInfo]:
        """Detect devices on Windows systems."""
        devices = []
        
        try:
            # Use PowerShell to get disk information
            ps_command = """
            Get-CimInstance -ClassName Win32_DiskDrive | 
            Select-Object DeviceID, Model, SerialNumber, Size, InterfaceType |
            ConvertTo-Json
            """
            
            result = subprocess.run(
                ['powershell', '-Command', ps_command],
                capture_output=True, text=True, check=True
            )
            
            import json
            data = json.loads(result.stdout)
            
            if isinstance(data, list):
                for disk in data:
                    device_info = DeviceInfo(
                        name=disk.get('DeviceID', '').replace('\\\\.\\', ''),
                        path=disk.get('DeviceID', ''),
                        model=disk.get('Model', ''),
                        serial=disk.get('SerialNumber', ''),
                        size=str(disk.get('Size', 0)),
                        transport=disk.get('InterfaceType', ''),
                        media_type=self._get_media_type(disk),
                        is_encrypted=False,
                        encryption_always_on=False
                    )
                    devices.append(device_info)
                    
        except Exception as e:
            print(f"Error detecting Windows devices: {e}")
            # Fallback to virtual devices for safety
            return self._detect_virtual_devices()
        
        return devices
    
    def _detect_virtual_devices(self) -> List[DeviceInfo]:
        """Detect virtual devices for safe testing."""
        devices = []
        
        # Check for virtual media files
        virtual_media_dir = "/app/virtual_media"
        if os.path.exists(virtual_media_dir):
            for i in range(10):  # Check for vdisk0.img to vdisk9.img
                vdisk_path = f"{virtual_media_dir}/vdisk{i}.img"
                if os.path.exists(vdisk_path):
                    device_info = DeviceInfo(
                        name=f"VDISK{i}",
                        path=vdisk_path,
                        model="Sandbox VDisk",
                        serial=f"SBX-vdisk{i}",
                        size="2G",
                        transport="file",
                        media_type="Magnetic",
                        is_encrypted=False,
                        encryption_always_on=False
                    )
                    devices.append(device_info)
        
        return devices
    
    def _get_media_type(self, device: Dict) -> str:
        """Determine media type from device information."""
        model = device.get('model', '').lower()
        transport = device.get('tran', '').lower()
        
        if 'ssd' in model or 'nvme' in transport:
            return 'Flash'
        elif 'hdd' in model or 'ata' in transport:
            return 'Magnetic'
        else:
            return 'Unknown'

