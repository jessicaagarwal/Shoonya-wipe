#!/usr/bin/env python3
"""
Sandbox virtual media provider: file-backed disks for safe wiping in Docker.
"""

import os
from pathlib import Path
from typing import List, Dict, Any

DEFAULT_DIR = Path(os.environ.get("SAFEERASE_SANDBOX_DIR", "/app/virtual_media"))


def ensure_sandbox_disks(count: int = 2, size_gib: int = 2) -> List[Path]:
    DEFAULT_DIR.mkdir(parents=True, exist_ok=True)
    disks: List[Path] = []
    for i in range(count):
        p = DEFAULT_DIR / f"vdisk{i}.img"
        if not p.exists():
            with open(p, "wb") as f:
                f.truncate(size_gib * 1024 * 1024 * 1024)
        disks.append(p)
    return disks


def list_sandbox_devices() -> List[Dict[str, Any]]:
    count = int(os.environ.get("SANDBOX_VDISKS", "2"))
    size_gib = int(os.environ.get("SANDBOX_VDISK_SIZE_GIB", "2"))
    disks = ensure_sandbox_disks(count, size_gib)
    devices: List[Dict[str, Any]] = []
    for p in disks:
        size_bytes = p.stat().st_size
        size_str = f"{size_bytes // (1024**3)}G"
        devices.append(
            {
                "name": p.stem.upper(),
                "path": p.as_posix(),
                "size": size_str,
                "type": "disk",
                "model": "Sandbox VDisk",
                "serial": f"SBX-{p.stem}",
                "tran": "file",
                "sandbox": True,
            }
        )
    return devices


def overwrite_file(path: Path, pattern: bytes = b"\x00", chunk_size: int = 1024 * 1024) -> Dict[str, Any]:
    """Overwrite file with pattern and return verification details."""
    verification_details = []
    
    try:
        with open(path, "r+b") as f:
            size = path.stat().st_size
            written = 0
            buf = pattern * (chunk_size // len(pattern))
            
            verification_details.append(f"Starting overwrite of {size} bytes")
            verification_details.append(f"Pattern: {pattern.hex()}")
            
            while written < size:
                to_write = min(chunk_size, size - written)
                f.write(buf[:to_write])
                written += to_write
                
                # Progress update every 10%
                if written % (size // 10) == 0:
                    verification_details.append(f"Progress: {written // (1024*1024)}MB / {size // (1024*1024)}MB")
            
            f.flush()
            os.fsync(f.fileno())
            
            verification_details.append("Overwrite completed successfully")
            verification_details.append(f"Total bytes written: {written}")
            verification_details.append("File system sync completed")
            
            return {
                "success": True,
                "verification_details": verification_details,
                "bytes_written": written
            }
    except Exception as e:
        verification_details.append(f"Error during overwrite: {str(e)}")
        return {
            "success": False,
            "verification_details": verification_details,
            "error": str(e)
        }


def cryptographic_erase_file(path: Path) -> Dict[str, Any]:
    """Simulate cryptographic erase and return verification details."""
    verification_details = []
    
    try:
        import os as _os
        chunk = 16 * 1024 * 1024
        size = path.stat().st_size
        
        verification_details.append(f"Starting cryptographic erase simulation on {size} bytes")
        verification_details.append("Simulating encryption key destruction")
        
        with open(path, "r+b") as f:
            # Overwrite first 16 MiB with random data
            f.seek(0)
            first_chunk_size = min(chunk, size)
            random_data = _os.urandom(first_chunk_size)
            f.write(random_data)
            verification_details.append(f"Overwrote first {first_chunk_size} bytes with random data")
            
            # Overwrite last 16 MiB with random data
            if size > chunk:
                f.seek(max(0, size - chunk))
                last_chunk_size = min(chunk, size - chunk)
                random_data = _os.urandom(last_chunk_size)
                f.write(random_data)
                verification_details.append(f"Overwrote last {last_chunk_size} bytes with random data")
            
            f.flush()
            os.fsync(f.fileno())
            
            verification_details.append("Cryptographic erase simulation completed")
            verification_details.append("Encryption key destruction simulated")
            verification_details.append("File system sync completed")
            
            return {
                "success": True,
                "verification_details": verification_details,
                "bytes_processed": min(size, chunk * 2)
            }
    except Exception as e:
        verification_details.append(f"Error during cryptographic erase: {str(e)}")
        return {
            "success": False,
            "verification_details": verification_details,
            "error": str(e)
        }


