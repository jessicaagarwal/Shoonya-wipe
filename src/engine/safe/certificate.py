from typing import Dict, Any
from datetime import datetime
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent))

from src.core.safe.nist_compliance import NISTComplianceEngine, DeviceInfo, SanitizationResult, SanitizationMethod, SanitizationTechnique
from src.core.safe.safeerase import write_log, sign_json, render_nist_pdf_certificate


def build_and_emit_cert(device: Dict[str, Any], result: Dict[str, Any], operator_name: str, operator_title: str) -> Dict[str, str]:
    engine = NISTComplianceEngine()
    dev = DeviceInfo(
        name=device.get('name', 'N/A'),
        path=device.get('path', 'N/A'),
        model=device.get('model', 'Unknown'),
        serial=device.get('serial', 'Unknown'),
        size=device.get('size', 'Unknown'),
        transport=device.get('transport', 'unknown'),
        media_type=device.get('media_type', 'Unknown'),
    )
    sr = SanitizationResult(
        success=result.get('success', False),
        method=SanitizationMethod.CLEAR if result.get('method') == 'Clear' else SanitizationMethod.PURGE,
        technique=SanitizationTechnique.CRYPTOGRAPHIC_ERASE if 'Crypto' in result.get('technique','') else (
            SanitizationTechnique.SSD_SECURE_ERASE if 'Secure Erase' in result.get('technique','') else SanitizationTechnique.SINGLE_PASS_OVERWRITE
        ),
        verification_status='passed' if result.get('success') else 'failed',
        completion_time=datetime.utcnow(),
        verification_details=result.get('verification_details', []),
    )
    certificate = engine.generate_nist_certificate(dev, sr, operator_name, operator_title)

    # Log + sign
    selected = {
        'path': dev.path, 'name': dev.name, 'model': dev.model, 'serial': dev.serial,
        'tran': dev.transport, 'size': dev.size,
    }
    log = write_log({'selected': selected, 'result': result, 'certificate': certificate, 'timestamp_end': datetime.utcnow().isoformat()+ 'Z'})
    signed = sign_json({'selected': selected, 'result': result, 'certificate': certificate})
    signed_path = write_log(signed, filename='wipelog_signed.json')
    pdf_path = render_nist_pdf_certificate(certificate)
    return {'log': log, 'signed': signed_path, 'pdf': pdf_path}


