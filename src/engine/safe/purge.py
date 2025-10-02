from typing import Dict, Any
from .utils import running_in_docker, Device, exec_cmd
from pathlib import Path


def purge_secure_erase(device: Device) -> Dict[str, Any]:
    details: list[str] = []
    success = True
    if running_in_docker() or device.path.endswith('.img'):
        # Simulate secure erase by randomizing head/tail
        try:
            p = Path(device.path)
            size = p.stat().st_size
            with open(p, 'r+b') as f:
                import os
                chunk = 16 * 1024 * 1024
                f.seek(0); f.write(os.urandom(min(chunk, size)))
                if size > chunk:
                    f.seek(max(0, size - chunk)); f.write(os.urandom(min(chunk, size)))
            details.append('Simulated SSD Secure Erase (head/tail randomized)')
        except Exception as e:
            success = False; details.append(f'Error: {e}')
    else:
        # Real hardware: try nvme format then hdparm
        if 'nvme' in device.transport.lower() or device.path.startswith('/dev/nvme'):
            rc, out, err = exec_cmd(['nvme', 'format', device.path, '-s1'])
            success = rc == 0; details.append(out or err)
        else:
            rc, out, err = exec_cmd(['hdparm', '--security-erase', 'NULL', device.path])
            success = rc == 0; details.append(out or err)
    return {
        'success': success,
        'verification_details': details,
        'method': 'Purge',
        'technique': 'SSD Secure Erase',
    }


def purge_crypto_erase(device: Device, always_encrypted: bool) -> Dict[str, Any]:
    details: list[str] = []
    success = True
    if not always_encrypted:
        return {
            'success': False,
            'verification_details': ['Drive not always-encrypted; CE not applicable'],
            'method': 'Purge',
            'technique': 'Cryptographic Erase',
        }
    if running_in_docker() or device.path.endswith('.img'):
        details.append('Simulated key destruction and metadata wipe')
        success = True
    else:
        rc, out, err = exec_cmd(['blkdiscard', device.path])
        success = rc == 0; details.append(out or err)
    return {
        'success': success,
        'verification_details': details,
        'method': 'Purge',
        'technique': 'Cryptographic Erase',
    }


