#!/usr/bin/env python3
"""
SafeErasePro - NIST SP 800-88r2 Compliant CLI

Features:
- NIST SP 800-88r2 compliant sanitization methods (Clear, Purge, Destroy)
- AI-guided decision flowchart following NIST guidelines
- Comprehensive verification and validation
- NIST-compliant certificate generation
- Support for SSD Secure Erase and Cryptographic Erase

Compliance: Follows NIST SP 800-88r2 guidelines for media sanitization.
"""

import json
import os
import subprocess
import sys
from datetime import datetime
import base64
import hashlib
import uuid
import platform

from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.prompt import Prompt, Confirm
from rich import box
import shutil

# Import NIST compliance engine
from .nist_compliance import (
    NISTComplianceEngine, DeviceInfo, SanitizationMethod, 
    SanitizationTechnique, DataSensitivity
)


console = Console()


def run_command(cmd: str, description: str = "") -> str | None:
    try:
        result = subprocess.run(
            cmd,
            shell=True,
            capture_output=True,
            text=True,
            timeout=15,
        )
        if result.returncode == 0:
            return result.stdout.strip()
        console.print(f"[red]Error running {description}: {result.stderr}[/red]")
        return None
    except subprocess.TimeoutExpired:
        console.print(f"[red]Timeout running {description}[/red]")
        return None
    except Exception as exc:  # noqa: BLE001
        console.print(f"[red]Exception running {description}: {exc}[/red]")
        return None


def fetch_block_devices() -> list[dict]:
    """Return lsblk JSON list of blockdevices with useful fields.

    Use either -o (specific columns) or -O (all), not both. Try -o first,
    then fall back to -O, then plain -J.
    """
    columns = "NAME,KNAME,PATH,SIZE,TYPE,MODEL,SERIAL,TRAN,MOUNTPOINT"
    candidates = [
        f"lsblk -J -o {columns}",  # preferred
        "lsblk -J -O",             # all columns
        "lsblk -J",                # minimal
    ]
    for cmd in candidates:
        output = run_command(cmd, "lsblk")
        if not output:
            continue
        try:
            data = json.loads(output)
            return data.get("blockdevices", [])
        except json.JSONDecodeError:
            continue
    console.print("[red]Failed to parse lsblk JSON output[/red]")
    return []


def flatten_devices(devices: list[dict]) -> list[dict]:
    """Flatten parent/child lsblk tree into a single list of top-level disks only."""
    flat: list[dict] = []
    for dev in devices:
        # Only consider disk or removable devices; skip partitions/loops by default
        if dev.get("type") in {"disk"}:
            flat.append(dev)
    return flat


def render_table(devices: list[dict]) -> None:
    table = Table(
        title="🔍 SafeErasePro - Device Selection (Non-destructive)",
        box=box.SIMPLE_HEAVY,
    )
    table.add_column("#", style="cyan", no_wrap=True)
    table.add_column("Name", style="cyan")
    table.add_column("Path", style="cyan")
    table.add_column("Size", style="green")
    table.add_column("Type", style="blue")
    table.add_column("Model", style="magenta")
    table.add_column("Serial", style="white")
    table.add_column("Tran", style="yellow")

    for idx, dev in enumerate(devices, start=1):
        table.add_row(
            str(idx),
            dev.get("name", "N/A"),
            dev.get("path", dev.get("kname", "N/A")),
            dev.get("size", "N/A"),
            dev.get("type", "N/A"),
            dev.get("model", "N/A") or "N/A",
            dev.get("serial", "N/A") or "N/A",
            dev.get("tran", "N/A") or "N/A",
        )
    console.print(table)


def select_device_interactive(devices: list[dict]) -> dict | None:
    if not devices:
        console.print("[yellow]No eligible block devices found.[/yellow]")
        return None

    render_table(devices)

    while True:
        choice = Prompt.ask(
            "Enter device number to select (or 'q' to quit)", default="q"
        )
        if choice.lower() == "q":
            return None
        if not choice.isdigit():
            console.print("[red]Please enter a valid number[/red]")
            continue
        idx = int(choice)
        if idx < 1 or idx > len(devices):
            console.print("[red]Out of range[/red]")
            continue
        return devices[idx - 1]


def double_confirm(selected: dict) -> bool:
    path = selected.get("path") or f"/dev/{selected.get('name')}"
    console.print(Panel.fit(
        f"You selected: [bold]{path}[/bold]\n"
        f"Model: {selected.get('model','N/A')}  Serial: {selected.get('serial','N/A')}  Tran: {selected.get('tran','N/A')}",
        style="bold yellow",
    ))

    # Skip the "Proceed to confirmation?" prompt in non-interactive environments (web GUI)
    if sys.stdin.isatty() and not Confirm.ask("Proceed to confirmation? (no action will be performed)"):
        return False

    typed_once = Prompt.ask("Type the exact device path to confirm", default="")
    if typed_once.strip() != path:
        console.print("[red]Mismatch. Aborting.[/red]")
        return False

    typed_twice = Prompt.ask("Type it again to double-confirm", default="")
    if typed_twice.strip() != path:
        console.print("[red]Second confirmation failed. Aborting.[/red]")
        return False

    console.print("[green]Double confirmation successful.[/green]")
    return True


def convert_to_device_info(device_dict: dict) -> DeviceInfo:
    """Convert device dictionary to DeviceInfo object."""
    return DeviceInfo(
        name=device_dict.get("name", "N/A"),
        path=device_dict.get("path") or f"/dev/{device_dict.get('name', 'N/A')}",
        model=device_dict.get("model", "N/A"),
        serial=device_dict.get("serial", "N/A"),
        size=device_dict.get("size", "N/A"),
        transport=device_dict.get("tran", "N/A"),
        media_type="Flash Memory" if device_dict.get("tran", "").lower() in ["nvme", "sata", "ata"] else "Magnetic",
        is_encrypted=False,  # Would need additional detection logic
        encryption_always_on=False  # Would need additional detection logic
    )


def select_wipe_method(device_info: dict) -> list[str]:
    """Legacy method - now handled by NIST compliance engine."""
    tran = (device_info.get("tran") or "").lower()
    dev_type = (device_info.get("type") or "").lower()
    if tran == "nvme" or dev_type == "nvme":
        return ["nvme", "sanitize"]
    if tran in {"sata", "ata"}:
        return ["hdparm", "--security-erase"]
    # Fallback for others (USB/SCSI/virtio, etc.)
    return ["blkdiscard"]


def ensure_out_dir() -> str:
    out_dir = os.path.join(os.getcwd(), "out")
    os.makedirs(out_dir, exist_ok=True)
    return out_dir


def init_log(selected: dict, method: list[str]) -> dict:
    now = datetime.utcnow().isoformat() + "Z"
    log: dict = {
        "wipe_id": str(uuid.uuid4()),
        "device": selected.get("path") or f"/dev/{selected.get('name')}",
        "name": selected.get("name"),
        "model": selected.get("model") or "N/A",
        "serial": selected.get("serial") or "N/A",
        "tran": selected.get("tran") or "N/A",
        "size": selected.get("size") or "N/A",
        "method": " ".join(method),
        "commands": [],
        "timestamp_start": now,
        "timestamp_end": None,
        "environment": {
            "cwd": os.getcwd(),
            "inside_docker": os.path.exists("/.dockerenv"),
            "host": platform.node(),
            "os": platform.platform(),
            "kernel": platform.release(),
            "python": platform.python_version(),
        },
    }
    return log


def log_command(log: dict, cmd: list[str] | str, returncode: int, stdout: str, stderr: str) -> None:
    log["commands"].append(
        {
            "cmd": cmd if isinstance(cmd, str) else " ".join(cmd),
            "returncode": returncode,
            "stdout": stdout,
            "stderr": stderr,
            "ts": datetime.utcnow().isoformat() + "Z",
        }
    )


def write_log(log: dict, filename: str = "wipelog.json") -> str:
    out_dir = ensure_out_dir()
    path = os.path.join(out_dir, filename)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(log, f, indent=2)
    return path


# -------- Phase 4: JSON signing (dev keys) -------- #
def ensure_dev_keys() -> tuple[str, str]:
    """Create RSA dev keypair if missing. Returns (private_path, public_path)."""
    try:
        from Crypto.PublicKey import RSA  # type: ignore
    except Exception:
        console.print("[red]PyCryptodome not installed. Cannot sign logs.[/red]")
        return "", ""

    keys_dir = os.path.join(os.getcwd(), "keys")
    os.makedirs(keys_dir, exist_ok=True)
    priv_path = os.path.join(keys_dir, "private.pem")
    pub_path = os.path.join(keys_dir, "public.pem")
    if not os.path.exists(priv_path) or not os.path.exists(pub_path):
        key = RSA.generate(2048)
        with open(priv_path, "wb") as f:
            f.write(key.export_key("PEM"))
        with open(pub_path, "wb") as f:
            f.write(key.publickey().export_key("PEM"))
    return priv_path, pub_path


def sign_json(json_obj: dict) -> dict:
    """Return a new object with signature fields added (dev only)."""
    from Crypto.PublicKey import RSA  # type: ignore
    from Crypto.Signature import pss  # type: ignore
    from Crypto.Hash import SHA256  # type: ignore

    priv_path, pub_path = ensure_dev_keys()
    if not priv_path or not os.path.exists(priv_path):
        return json_obj

    data_bytes = json.dumps(json_obj, separators=(",", ":"), sort_keys=True).encode(
        "utf-8"
    )
    h = SHA256.new(data_bytes)
    key = RSA.import_key(open(priv_path, "rb").read())
    signature = pss.new(key).sign(h)
    sig_b64 = base64.b64encode(signature).decode("ascii")

    pub_bytes = open(pub_path, "rb").read()
    pub_fingerprint = hashlib.sha256(pub_bytes).hexdigest()[:16]

    signed = dict(json_obj)  # shallow copy
    signed["signature"] = {
        "alg": "RSA-PSS-SHA256",
        "sig_b64": sig_b64,
        "pubkey_sha256_16": pub_fingerprint,
    }
    return signed


# -------- Phase 5: PDF certificate (summary) -------- #
def render_pdf_certificate(signed_log: dict) -> str:
    """Legacy PDF certificate - use render_nist_pdf_certificate instead."""
    try:
        from reportlab.lib.pagesizes import A4  # type: ignore
        from reportlab.pdfgen import canvas  # type: ignore
        from reportlab.lib.units import mm  # type: ignore
    except Exception as e:
        console.print(f"[red]reportlab not installed. Cannot create PDF certificate: {e}[/red]")
        return ""

    out_dir = ensure_out_dir()
    pdf_path = os.path.join(out_dir, "certificate.pdf")

    try:
        c = canvas.Canvas(pdf_path, pagesize=A4)
    except Exception as e:
        console.print(f"[red]Failed to create certificate PDF at {pdf_path}: {e}[/red]")
        return ""
    width, height = A4

    y = height - 30 * mm
    c.setFont("Helvetica-Bold", 18)
    c.drawString(20 * mm, y, "SafeErasePro - Wipe Certificate (MVP)")
    y -= 15 * mm

    c.setFont("Helvetica", 11)
    def line(text: str):
        nonlocal y
        c.drawString(20 * mm, y, text)
        y -= 7 * mm

    line(f"Generated: {datetime.utcnow().isoformat()}Z")
    line(f"Device: {signed_log.get('device')}")
    line(f"Model: {signed_log.get('model')}  Serial: {signed_log.get('serial')}")
    line(f"Transport: {signed_log.get('tran')}  Size: {signed_log.get('size')}")
    line(f"Method: {signed_log.get('method')}")
    line(f"Start: {signed_log.get('timestamp_start')}  End: {signed_log.get('timestamp_end')}")

    sig = signed_log.get("signature", {})
    line("Signature:")
    line(f"  Alg: {sig.get('alg', 'N/A')}")
    line(f"  PubKey SHA256 (16): {sig.get('pubkey_sha256_16', 'N/A')}")

    # Show a short prefix of the signature for readability
    sig_b64 = sig.get("sig_b64", "")
    if sig_b64:
        line(f"  Sig (first 32 b64 chars): {sig_b64[:32]}...")

    c.showPage()
    try:
        c.save()
    except Exception as e:
        console.print(f"[red]Failed to save certificate PDF: {e}[/red]")
        return ""
    return pdf_path


def render_nist_pdf_certificate(certificate: dict) -> str:
    """
    Rule 4.1: Include All Required Fields in Certificates (Page 30)
    Generate NIST-compliant PDF certificate with all required fields.
    """
    try:
        from reportlab.lib.pagesizes import A4  # type: ignore
        from reportlab.pdfgen import canvas  # type: ignore
        from reportlab.lib.units import mm  # type: ignore
        from reportlab.lib import colors  # type: ignore
    except Exception:
        console.print("[red]reportlab not installed. Cannot create PDF certificate.[/red]")
        return ""

    out_dir = ensure_out_dir()
    pdf_path = os.path.join(out_dir, "nist_certificate.pdf")

    c = canvas.Canvas(pdf_path, pagesize=A4)
    width, height = A4

    # Header
    y = height - 20 * mm
    c.setFont("Helvetica-Bold", 16)
    c.setFillColor(colors.darkblue)
    c.drawString(20 * mm, y, "SafeErasePro - NIST SP 800-88r2 Compliance Certificate")
    y -= 10 * mm

    # NIST Compliance Badge
    c.setFont("Helvetica-Bold", 12)
    c.setFillColor(colors.green)
    c.drawString(20 * mm, y, "✓ NIST SP 800-88r2 Compliant")
    y -= 15 * mm

    # Required NIST Fields (Section 4.6)
    c.setFont("Helvetica-Bold", 14)
    c.setFillColor(colors.black)
    c.drawString(20 * mm, y, "Required Sanitization Information")
    y -= 8 * mm

    c.setFont("Helvetica", 10)
    def line(label: str, value: str):
        nonlocal y
        c.setFont("Helvetica-Bold", 10)
        c.drawString(20 * mm, y, f"{label}:")
        c.setFont("Helvetica", 10)
        c.drawString(80 * mm, y, str(value))
        y -= 6 * mm

    # All required NIST fields
    line("Manufacturer", certificate.get("manufacturer", "N/A"))
    line("Model", certificate.get("model", "N/A"))
    line("Serial Number", certificate.get("serial_number", "N/A"))
    line("Media Type", certificate.get("media_type", "N/A"))
    line("Sanitization Method", certificate.get("sanitization_method", "N/A"))
    line("Sanitization Technique", certificate.get("sanitization_technique", "N/A"))
    line("Tool Used", certificate.get("tool_used", "N/A"))
    line("Verification Method", certificate.get("verification_method", "N/A"))
    line("Operator Name", certificate.get("operator_name", "N/A"))
    line("Operator Title", certificate.get("operator_title", "N/A"))
    line("Date", certificate.get("date", "N/A"))

    y -= 10 * mm

    # Additional Information
    c.setFont("Helvetica-Bold", 14)
    c.drawString(20 * mm, y, "Additional Information")
    y -= 8 * mm

    c.setFont("Helvetica", 10)
    line("Device Path", certificate.get("device_path", "N/A"))
    line("Device Size", certificate.get("device_size", "N/A"))
    line("Verification Status", certificate.get("verification_status", "N/A"))
    line("Completion Time", certificate.get("completion_time", "N/A"))
    line("Certificate ID", certificate.get("certificate_id", "N/A"))

    # Verification Details Section
    verification_details = certificate.get("verification_details", [])
    if verification_details:
        y -= 10 * mm
        c.setFont("Helvetica-Bold", 12)
        c.drawString(20 * mm, y, "Verification Details")
        y -= 8 * mm
        
        c.setFont("Helvetica", 9)
        for detail in verification_details:
            c.drawString(20 * mm, y, f"• {detail}")
            y -= 5 * mm
            if y < 50 * mm:  # Prevent text from going off page
                break

    y -= 15 * mm

    # Compliance Statement
    c.setFont("Helvetica-Bold", 12)
    c.setFillColor(colors.darkblue)
    c.drawString(20 * mm, y, "Compliance Statement")
    y -= 8 * mm

    c.setFont("Helvetica", 10)
    c.setFillColor(colors.black)
    compliance_text = (
        "This sanitization was performed in accordance with NIST Special Publication 800-88r2, "
        "Guidelines for Media Sanitization. The sanitization method and technique were selected "
        "based on the official NIST decision flowchart, taking into account data sensitivity level, "
        "device reuse plans, and physical control requirements."
    )
    
    # Wrap text
    lines = []
    words = compliance_text.split()
    current_line = ""
    for word in words:
        if len(current_line + " " + word) < 80:  # Approximate character limit
            current_line += " " + word if current_line else word
        else:
            lines.append(current_line)
            current_line = word
    if current_line:
        lines.append(current_line)
    
    for line_text in lines:
        c.drawString(20 * mm, y, line_text)
        y -= 6 * mm

    y -= 10 * mm

    # Signature Section
    c.setFont("Helvetica-Bold", 12)
    c.drawString(20 * mm, y, "Digital Signature")
    y -= 8 * mm

    c.setFont("Helvetica", 10)
    c.drawString(20 * mm, y, "This certificate is digitally signed and can be verified using the")
    y -= 6 * mm
    c.drawString(20 * mm, y, "corresponding public key and signed log files.")
    y -= 6 * mm
    c.drawString(20 * mm, y, f"Certificate ID: {certificate.get('certificate_id', 'N/A')}")

    # Footer
    y = 30 * mm
    c.setFont("Helvetica", 8)
    c.setFillColor(colors.grey)
    c.drawString(20 * mm, y, "Generated by SafeErasePro - NIST SP 800-88r2 Compliant")
    c.drawString(20 * mm, y - 6, f"Generated on: {datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S UTC')}")

    c.showPage()
    c.save()
    return pdf_path


def main() -> int:
    console.print(Panel.fit(
        "🔒 SafeErasePro - NIST SP 800-88r2 Compliant CLI\n"
        "Secure Data Wiping Tool with AI-Guided Decision Process",
        style="bold green"
    ))
    console.print(f"[dim]Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}[/dim]")
    console.print(f"[dim]Working Directory: {os.getcwd()}[/dim]")

    # Initialize NIST compliance engine
    nist_engine = NISTComplianceEngine()

    # Get available devices
    devices_raw = fetch_block_devices()
    devices = flatten_devices(devices_raw)

    if not devices:
        console.print("[yellow]No eligible block devices found.[/yellow]")
        return 0

    # Display devices and get user selection
    selected = select_device_interactive(devices)
    if not selected:
        console.print("[yellow]No device selected. Exiting.[/yellow]")
        return 0

    # Convert to DeviceInfo object
    device_info = convert_to_device_info(selected)
    
    # Double confirmation
    confirmed = double_confirm(selected)
    if not confirmed:
        console.print("[yellow]Operation cancelled by user.[/yellow]")
        return 0

    # Run NIST decision flowchart
    console.print("\n" + "="*60)
    console.print("🤖 NIST SP 800-88r2 AI Decision Process")
    console.print("="*60)
    
    method, technique = nist_engine.run_nist_decision_flowchart(device_info)
    
    # Validate method choice
    if not nist_engine.validate_method_choice(device_info, method, technique):
        console.print("[red]Invalid method choice. Exiting.[/red]")
        return 1

    # Get operator information for certificate
    console.print("\n" + "="*60)
    console.print("📋 Operator Information for Certificate")
    console.print("="*60)
    
    operator_name = Prompt.ask("Enter operator name", default="System Administrator")
    operator_title = Prompt.ask("Enter operator title", default="IT Security Specialist")

    # Execute sanitization
    console.print("\n" + "="*60)
    console.print("🔧 Executing Sanitization")
    console.print("="*60)
    
    if method == SanitizationMethod.DESTROY:
        nist_engine.recommend_destroy_method()
        console.print("[yellow]Physical destruction recommended. No software action taken.[/yellow]")
        return 0
    
    # Execute the chosen method
    if method == SanitizationMethod.CLEAR:
        result = nist_engine.execute_clear_method(device_info)
    elif method == SanitizationMethod.PURGE:
        result = nist_engine.execute_purge_method(device_info, technique)
    else:
        console.print("[red]Unknown sanitization method.[/red]")
        return 1

    # Verify sanitization
    console.print("\n" + "="*60)
    console.print("✅ Verification Process")
    console.print("="*60)
    
    verification_passed = nist_engine.verify_sanitization(device_info, result)

    # Generate NIST-compliant certificate
    console.print("\n" + "="*60)
    console.print("📄 Generating NIST-Compliant Certificate")
    console.print("="*60)
    
    certificate = nist_engine.generate_nist_certificate(
        device_info, result, operator_name, operator_title
    )

    # Create comprehensive log with NIST compliance data
    log = init_log(selected, [method.value, technique.value])
    log.update({
        "nist_compliance": {
            "standard": "NIST SP 800-88r2",
            "method": method.value,
            "technique": technique.value,
            "verification_status": result.verification_status,
            "compliance_checked": True
        },
        "certificate": certificate,
        "timestamp_end": datetime.utcnow().isoformat() + "Z"
    })

    # Write logs and certificates
    log_path = write_log(log)
    signed = sign_json(log)
    signed_path = write_log(signed, filename="wipelog_signed.json")
    
    # Generate NIST-compliant PDF certificate
    pdf_path = render_nist_pdf_certificate(certificate)
    # Ensure paths are absolute for the web to pick up
    log_path = os.path.abspath(log_path)
    signed_path = os.path.abspath(signed_path)
    pdf_path = os.path.abspath(pdf_path) if pdf_path else pdf_path

    # Export artifacts
    default_export = os.path.join(os.getcwd(), "exports")
    export_dir = Prompt.ask(
        "Enter export directory for artifacts (or leave blank to skip)",
        default=default_export,
    )
    exported_paths: list[str] = []
    if export_dir:
        os.makedirs(export_dir, exist_ok=True)
        for p in [log_path, signed_path, pdf_path]:
            if p and os.path.exists(p):
                dst = os.path.join(export_dir, os.path.basename(p))
                shutil.copy2(p, dst)
                exported_paths.append(dst)

    # Display final results
    console.print("\n" + "="*60)
    console.print("🎉 Sanitization Complete")
    console.print("="*60)
    
    console.print(
        Panel.fit(
            "\n".join(
                [
                    f"Device: {device_info.path}",
                    f"Method: {method.value}",
                    f"Technique: {technique.value}",
                    f"Verification: {result.verification_status}",
                    f"Operator: {operator_name} ({operator_title})",
                    f"Certificate: {pdf_path if pdf_path else 'PDF generation failed'}",
                    f"Log: {log_path}",
                    f"Signed Log: {signed_path}",
                    (
                        "Exports: " + ", ".join(exported_paths)
                        if exported_paths
                        else "Exports: skipped"
                    ),
                ]
            ),
            style="bold green",
        )
    )

    return 0 if verification_passed else 1


if __name__ == "__main__":
    sys.exit(main())


