#!/usr/bin/env python3
"""
Script to send email using the MCP Agent.
"""

import requests
import json
import os
from pathlib import Path

def send_email_from_file(file_path: str) -> None:
    """Send an email using the MCP Agent and a text file.
    
    Args:
        file_path: Path to the email text file
    """
    # Ensure the file exists
    if not os.path.exists(file_path):
        print(f"Error: File not found: {file_path}")
        return

    # Prepare the request
    url = "http://127.0.0.1:8000/tools/send_email_from_file"
    headers = {
        "Content-Type": "application/json",
        "X-API-Key": "demo-secret-key"
    }
    data = {
        "data": {
            "file_path": str(Path(file_path).absolute())
        }
    }

    try:
        # Send the request
        print(f"Sending email using file: {file_path}")
        response = requests.post(url, headers=headers, json=data)
        
        # Check the response
        if response.status_code == 200:
            result = response.json()
            if result.get("status") == "success":
                print("Email sent successfully!")
                print("Details:", json.dumps(result.get("data", {}), indent=2))
            else:
                print("Error sending email:", result.get("message", "Unknown error"))
        else:
            print(f"Error: HTTP {response.status_code}")
            print(response.text)

    except requests.exceptions.ConnectionError:
        print("Error: Could not connect to the MCP Agent. Make sure it's running on port 8000.")
    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    # Get the current directory
    current_dir = Path(__file__).parent
    
    # Path to the sample email file
    email_file = current_dir / "sample_email.txt"
    
    # Send the email
    send_email_from_file(email_file) 