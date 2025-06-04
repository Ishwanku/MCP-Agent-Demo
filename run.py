#!/usr/bin/env python3
"""
MCP Agent Demo Runner Script

This script handles the complete setup and execution of the MCP Agent Demo:
1. Checks Python version
2. Creates/activates virtual environment
3. Installs dependencies
4. Starts the MCP Agent
"""

import os
import sys
import subprocess
import platform
from pathlib import Path

def check_python_version():
    """Check if Python version is compatible."""
    if sys.version_info < (3, 9):
        print("Error: Python 3.9 or higher is required")
        sys.exit(1)

def get_venv_path():
    """Get the virtual environment path."""
    return Path(".venv")

def create_venv():
    """Create virtual environment if it doesn't exist."""
    venv_path = get_venv_path()
    if not venv_path.exists():
        print("Creating virtual environment...")
        subprocess.run([sys.executable, "-m", "venv", str(venv_path)], check=True)
        
        # Ensure pip is installed in the virtual environment
        python = get_venv_python()
        print("Ensuring pip is installed...")
        try:
            # First try to upgrade pip
            subprocess.run([str(python), "-m", "ensurepip", "--upgrade"], check=True)
        except subprocess.CalledProcessError:
            # If that fails, try to install pip
            subprocess.run([str(python), "-m", "ensurepip"], check=True)

def get_venv_python():
    """Get the Python executable from virtual environment."""
    venv_path = get_venv_path()
    if platform.system() == "Windows":
        return venv_path / "Scripts" / "python.exe"
    return venv_path / "bin" / "python"

def install_dependencies():
    """Install required dependencies."""
    print("Installing dependencies...")
    python = get_venv_python()
    
    # First upgrade pip itself
    print("Upgrading pip...")
    subprocess.run([str(python), "-m", "pip", "install", "--upgrade", "pip"], check=True)
    
    # Then install the package
    print("Installing MCP Agent Demo...")
    subprocess.run([str(python), "-m", "pip", "install", "-e", "."], check=True)

def start_agent():
    """Start the MCP Agent."""
    print("Starting MCP Agent...")
    python = get_venv_python()
    subprocess.run([str(python), "-m", "mcp.agents.demo_agent"], check=True)

def main():
    """Main function to run the setup and start the agent."""
    try:
        print("Setting up MCP Agent Demo...")
        check_python_version()
        create_venv()
        install_dependencies()
        start_agent()
    except subprocess.CalledProcessError as e:
        print(f"Error during setup: {e}")
        print("\nTroubleshooting steps:")
        print("1. Make sure you have Python 3.9 or higher installed")
        print("2. Try deleting the .venv folder and running the script again")
        print("3. Check if you have write permissions in the current directory")
        sys.exit(1)
    except Exception as e:
        print(f"Unexpected error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main() 