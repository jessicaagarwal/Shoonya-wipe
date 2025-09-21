import os
import subprocess
from dataclasses import dataclass
from typing import Optional


def running_in_docker() -> bool:
    return os.path.exists("/.dockerenv") or os.environ.get("RUNNING_IN_DOCKER") == "1"


@dataclass
class Device:
    name: str
    path: str
    model: str = "Unknown"
    serial: str = "Unknown"
    size: str = "Unknown"
    transport: str = "unknown"
    media_type: str = "Unknown"


def exec_cmd(cmd: list[str]) -> tuple[int, str, str]:
    try:
        p = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, check=False)
        return p.returncode, p.stdout, p.stderr
    except Exception as e:
        return 1, "", str(e)


