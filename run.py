#!/usr/bin/env python3
"""Cross-platform launcher for Convertex. Works on Windows, macOS, and Linux."""

import os
import subprocess
import sys
from pathlib import Path


def main() -> int:
    root = Path(__file__).resolve().parent
    os.chdir(root)

    venv_dir = root / ".venv"
    if not venv_dir.exists():
        print("Creating virtual environment...")
        subprocess.check_call([sys.executable, "-m", "venv", str(venv_dir)])

    if sys.platform == "win32":
        pip = venv_dir / "Scripts" / "pip.exe"
        streamlit = venv_dir / "Scripts" / "streamlit.exe"
    else:
        pip = venv_dir / "bin" / "pip"
        streamlit = venv_dir / "bin" / "streamlit"

    print("Installing dependencies...")
    subprocess.run(
        [str(pip), "install", "-q", "-r", "requirements.txt"],
        check=True,
        capture_output=True,
    )

    print("\nStarting Convertex...")
    print("  Local:   http://localhost:8501")
    if sys.platform != "win32":
        try:
            import socket
            hostname = socket.gethostname()
            ip = socket.gethostbyname(hostname)
            if ip and not ip.startswith("127."):
                print(f"  Network: http://{ip}:8501")
        except Exception:
            pass
    print()

    return subprocess.call([
        str(streamlit),
        "run",
        "app.py",
        "--server.headless=true",
        "--server.port=8501",
    ])


if __name__ == "__main__":
    sys.exit(main())
