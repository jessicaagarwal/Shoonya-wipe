from pathlib import Path
from typing import Dict, Any
from .utils import running_in_docker, Device


def clear_overwrite(device: Device) -> Dict[str, Any]:
    """Single-pass overwrite. Simulation in Docker; real write on Linux file path."""
    details: list[str] = []
    success = True
    bytes_written = 0

    try:
        if running_in_docker() or device.path.endswith(".img"):
            # File-backed simulation
            p = Path(device.path)
            if not p.exists():
                raise FileNotFoundError(str(p))
            size = p.stat().st_size
            details.append(f"Starting overwrite of {size} bytes")
            with open(p, "r+b") as f:
                chunk = b"\x00" * (1024 * 1024)
                remaining = size
                while remaining > 0:
                    n = min(len(chunk), remaining)
                    f.write(chunk[:n])
                    bytes_written += n
                    remaining -= n
            details.append("Overwrite completed")
        else:
            # Real device path: use dd
            from .utils import exec_cmd
            rc, out, err = exec_cmd(["dd", f"if=/dev/zero", f"of={device.path}", "bs=1M", "status=none"])
            success = rc == 0
            details.append(out or err or "dd completed")
    except Exception as e:
        success = False
        details.append(f"Error: {e}")

    return {
        "success": success,
        "verification_details": details,
        "bytes_written": bytes_written,
        "method": "Clear",
        "technique": "Single Pass Overwrite",
    }


