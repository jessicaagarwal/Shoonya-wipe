def get_devices() -> List[Dict[str, Any]]:
    """Get list of available devices using lsblk."""
    # Sandbox mode - detect real drives but will simulate wipe
    print("DEBUG: Sandbox mode - detecting real drives but will simulate wipe")
    
    # Detect real devices but mark them as sandbox for simulation
    if os.name == "nt":  # Windows
        print("DEBUG: Detecting Windows devices...")
        try:
            # Try PowerShell CIM -> JSON
            cmd = [
                "powershell", "-Command",
                "Get-CimInstance -ClassName Win32_DiskDrive | Select-Object DeviceID, Model, SerialNumber, Size, InterfaceType | ConvertTo-Json"
            ]
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=10)
            print(f"DEBUG: PowerShell result code: {result.returncode}")
            print(f"DEBUG: PowerShell stdout: {result.stdout}")
            print(f"DEBUG: PowerShell stderr: {result.stderr}")
            
            if result.returncode == 0 and result.stdout.strip():
                try:
                    data = json.loads(result.stdout)
                    if not isinstance(data, list):
                        data = [data]
                    
                    devices = []
                    for drive in data:
                        if drive.get("DeviceID"):
                            size_gb = int(drive.get("Size", 0)) // (1024**3)
                            device_info = {
                                "name": drive["DeviceID"].split("\\")[-1],
                                "path": f"sandbox:{drive['DeviceID']}",  # Prefix for sandbox mode
                                "model": drive.get("Model", "Unknown"),
                                "serial": drive.get("SerialNumber", "Unknown"),
                                "size": f"{size_gb}G",
                                "transport": drive.get("InterfaceType", "Unknown"),
                                "media_type": "Magnetic",
                                "is_encrypted": False,
                                "encryption_always_on": False
                            }
                            devices.append(device_info)
                    
                    print(f"DEBUG: Found {len(devices)} Windows devices (sandbox mode)")
                    return devices
                except json.JSONDecodeError as e:
                    print(f"DEBUG: JSON decode error: {e}")
            
            # Fallback to WMIC
            cmd = ["wmic", "diskdrive", "get", "DeviceID,Model,SerialNumber,Size,InterfaceType", "/format:csv"]
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=10)
            print(f"DEBUG: WMIC result code: {result.returncode}")
            print(f"DEBUG: WMIC stdout: {result.stdout}")
            print(f"DEBUG: WMIC stderr: {result.stderr}")
            
            if result.returncode == 0:
                devices = []
                lines = result.stdout.strip().split('\n')
                for line in lines[1:]:  # Skip header
                    if line.strip():
                        parts = line.split(',')
                        if len(parts) >= 6 and parts[1]:  # DeviceID exists
                            size_gb = int(parts[4]) // (1024**3) if parts[4].isdigit() else 0
                            device_info = {
                                "name": parts[1].split("\\")[-1],
                                "path": f"sandbox:{parts[1]}",  # Prefix for sandbox mode
                                "model": parts[2] if len(parts) > 2 else "Unknown",
                                "serial": parts[3] if len(parts) > 3 else "Unknown",
                                "size": f"{size_gb}G",
                                "transport": parts[5] if len(parts) > 5 else "Unknown",
                                "media_type": "Magnetic",
                                "is_encrypted": False,
                                "encryption_always_on": False
                            }
                            devices.append(device_info)
                
                print(f"DEBUG: Found {len(devices)} Windows devices via WMIC (sandbox mode)")
                return devices
                
        except Exception as e:
            print(f"DEBUG: Windows device detection failed: {e}")
    
    # Linux fallback
    try:
        result = subprocess.run(['lsblk', '-J'], capture_output=True, text=True, timeout=10)
        if result.returncode == 0:
            data = json.loads(result.stdout)
            devices = []
            for device in data.get('blockdevices', []):
                if device.get('type') == 'disk' and not device.get('children'):
                    size = device.get('size', '0')
                    device_info = {
                        "name": device['name'],
                        "path": f"sandbox:/dev/{device['name']}",  # Prefix for sandbox mode
                        "model": device.get('model', 'Unknown'),
                        "serial": device.get('serial', 'Unknown'),
                        "size": size,
                        "transport": device.get('tran', 'Unknown'),
                        "media_type": "Magnetic",
                        "is_encrypted": False,
                        "encryption_always_on": False
                    }
                    devices.append(device_info)
            print(f"DEBUG: Found {len(devices)} Linux devices (sandbox mode)")
            return devices
    except Exception as e:
        print(f"DEBUG: Linux device detection failed: {e}")
    
    # Final fallback to sandbox devices
    print("DEBUG: Falling back to sandbox devices")
    return list_sandbox_devices()

