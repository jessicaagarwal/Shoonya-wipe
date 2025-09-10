#!/usr/bin/env python3
"""
SafeErasePro - Device Scanner Test Script
This script demonstrates basic device detection capabilities in a safe Docker environment.
"""

import subprocess
import json
import sys
import os
from datetime import datetime
from rich.console import Console
from rich.table import Table
from rich.panel import Panel

console = Console()

def run_command(cmd, description=""):
    """Safely run a system command and return output."""
    try:
        result = subprocess.run(
            cmd, 
            shell=True, 
            capture_output=True, 
            text=True, 
            timeout=10
        )
        if result.returncode == 0:
            return result.stdout.strip()
        else:
            console.print(f"[red]Error running {description}: {result.stderr}[/red]")
            return None
    except subprocess.TimeoutExpired:
        console.print(f"[red]Timeout running {description}[/red]")
        return None
    except Exception as e:
        console.print(f"[red]Exception running {description}: {e}[/red]")
        return None

def get_block_devices():
    """Get list of block devices using lsblk."""
    cmd = "lsblk -J -o NAME,SIZE,TYPE,MOUNTPOINT,MODEL,SERIAL"
    output = run_command(cmd, "lsblk")
    
    if not output:
        return []
    
    try:
        data = json.loads(output)
        return data.get('blockdevices', [])
    except json.JSONDecodeError:
        console.print("[red]Failed to parse lsblk JSON output[/red]")
        return []

def get_disk_info():
    """Get additional disk information."""
    info = {}
    
    # Get disk usage
    df_output = run_command("df -h", "disk usage")
    if df_output:
        info['disk_usage'] = df_output.split('\n')
    
    # Get memory info
    meminfo = run_command("cat /proc/meminfo | head -5", "memory info")
    if meminfo:
        info['memory'] = meminfo.split('\n')
    
    # Get CPU info (portable across x86/ARM, including macOS hosts via Docker)
    # Try multiple sources since ARM cpuinfo may not have 'model name'
    cpuinfo = run_command(
        "cat /proc/cpuinfo | grep -m1 -E 'model name|Hardware|Processor' | sed 's/^.*:\\s*//'",
        "CPU info (/proc/cpuinfo)")
    if not cpuinfo:
        cpuinfo = run_command(
            "lscpu | grep -m1 -E 'Model name|Architecture' | sed 's/^.*:\\s*//'",
            "CPU info (lscpu)")
    if not cpuinfo:
        cpuinfo = run_command("uname -m", "CPU architecture (uname)")
    if cpuinfo:
        info['cpu'] = cpuinfo
    
    return info

def display_device_table(devices):
    """Display devices in a nice table format."""
    if not devices:
        console.print("[yellow]No block devices found[/yellow]")
        return
    
    table = Table(title="🔍 SafeErasePro - Block Device Scanner")
    table.add_column("Device", style="cyan", no_wrap=True)
    table.add_column("Size", style="green")
    table.add_column("Type", style="blue")
    table.add_column("Mount Point", style="yellow")
    table.add_column("Model", style="magenta")
    table.add_column("Serial", style="white")
    
    for device in devices:
        name = device.get('name', 'N/A')
        size = device.get('size', 'N/A')
        device_type = device.get('type', 'N/A')
        mountpoint = device.get('mountpoint', 'N/A') or 'Not mounted'
        model = device.get('model', 'N/A')
        serial = device.get('serial', 'N/A')
        
        table.add_row(name, size, device_type, mountpoint, model, serial)
    
    console.print(table)

def display_system_info(info):
    """Display additional system information."""
    console.print("\n" + "="*60)
    console.print(Panel.fit("🖥️  System Information", style="bold blue"))
    
    if 'cpu' in info:
        console.print(f"[bold]CPU:[/bold] {info['cpu']}")
    
    if 'memory' in info:
        console.print("[bold]Memory:[/bold]")
        for line in info['memory']:
            if line.strip():
                console.print(f"  {line}")
    
    if 'disk_usage' in info:
        console.print("[bold]Disk Usage:[/bold]")
        for line in info['disk_usage']:
            if line.strip():
                console.print(f"  {line}")

def main():
    """Main function to run the device scanner."""
    console.print(Panel.fit(
        "SafeErasePro Development Environment\n"
        "🔒 Safe Device Scanner - Docker Sandbox Mode",
        style="bold green"
    ))
    
    console.print(f"[dim]Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}[/dim]")
    console.print(f"[dim]Python Version: {sys.version}[/dim]")
    console.print(f"[dim]Working Directory: {os.getcwd()}[/dim]")
    
    # Check if we're running in Docker
    if os.path.exists('/.dockerenv'):
        console.print("[green]✅ Running inside Docker container[/green]")
    else:
        console.print("[yellow]⚠️  Not running in Docker - this is for development only[/yellow]")
    
    console.print("\n" + "="*60)
    
    # Get and display block devices
    devices = get_block_devices()
    display_device_table(devices)
    
    # Get and display system info
    system_info = get_disk_info()
    display_system_info(system_info)
    
    # Summary
    console.print("\n" + "="*60)
    console.print(Panel.fit(
        f"📊 Scan Complete\n"
        f"Found {len(devices)} block device(s)\n"
        f"Environment: {'Docker' if os.path.exists('/.dockerenv') else 'Host OS'}",
        style="bold green"
    ))
    
    # Safety warning
    console.print("\n[bold red]⚠️  SAFETY WARNING:[/bold red]")
    console.print("This is a development environment scanner only.")
    console.print("No actual data wiping operations are performed.")
    console.print("Always test in a safe, isolated environment first.")

if __name__ == "__main__":
    main()
