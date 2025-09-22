from typing import Dict, Any
from .utils import Device, running_in_docker
from .clear import clear_overwrite
from .purge import purge_secure_erase, purge_crypto_erase
from .certificate import build_and_emit_cert


def decide_method(device: Device, always_encrypted: bool = False) -> Dict[str, str]:
    # One-click heuristic
    if device.transport.lower() in ["nvme", "sata", "ata"]:
        return {"method": "Purge", "technique": "SSD Secure Erase"}
    if always_encrypted:
        return {"method": "Purge", "technique": "Cryptographic Erase"}
    return {"method": "Clear", "technique": "Single Pass Overwrite"}


def execute(device: Device, operator_name: str, operator_title: str, always_encrypted: bool = False) -> Dict[str, Any]:
    choice = decide_method(device, always_encrypted)
    if choice["method"] == "Purge":
        if choice["technique"] == "SSD Secure Erase":
            result = purge_secure_erase(device)
        else:
            result = purge_crypto_erase(device, always_encrypted)
    else:
        result = clear_overwrite(device)

    artifacts = build_and_emit_cert(
        {
            'name': device.name, 'path': device.path, 'model': device.model,
            'serial': device.serial, 'size': device.size, 'transport': device.transport,
            'media_type': device.media_type,
        },
        result,
        operator_name,
        operator_title,
    )

    return {"choice": choice, "result": result, "artifacts": artifacts}


