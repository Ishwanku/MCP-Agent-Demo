"""
Email tool implementation for the MCP Agent.

This module provides functionality to send emails using Microsoft Outlook through COM automation.
It handles automatic Outlook startup, email composition, and sending with support for attachments,
CC, and BCC recipients.

Key Features:
- Automatic Outlook startup and management
- Email composition with rich text support
- Multiple recipient handling (To, CC, BCC)
- File attachment support
- Comprehensive error handling and logging
- Windows path normalization

Dependencies:
- win32com: For Outlook COM automation
- psutil: For process management
- pydantic: For configuration management

Example:
    ```python
    email_tool = EmailTool()
    result = email_tool.send_email({
        'to': ['recipient@example.com'],
        'subject': 'Test Email',
        'body': 'Hello, World!',
        'cc': ['cc@example.com'],
        'attachments': ['path/to/file.pdf']
    })
    ```

Configuration:
    The tool requires the following environment variables:
    - OUTLOOK_PATH: Path to the Outlook executable
"""

import win32com.client
from typing import Dict, Any, List, Optional
from datetime import datetime
import os
import subprocess
import time
from mcp.core.config import settings

class EmailTool:
    """A tool for sending emails using Microsoft Outlook.
    
    This class provides a high-level interface for sending emails through Outlook,
    handling all the complexities of COM automation, process management, and error handling.
    
    Attributes:
        outlook: The Outlook COM object instance
        namespace: The Outlook namespace object for accessing mail items
        
    Methods:
        __init__: Initialize the email tool and set up Outlook path
        _ensure_outlook_running: Ensure Outlook is running, start if necessary
        send_email: Send an email with the provided data
    """

    def __init__(self):
        """Initialize the email tool.
        
        Sets up the Outlook path in the environment and initializes COM objects.
        The Outlook path is taken from the settings and added to the system PATH
        if it exists.
        """
        outlook_path = settings.OUTLOOK_PATH
        if outlook_path and os.path.exists(outlook_path):
            os.environ["PATH"] += os.pathsep + os.path.dirname(outlook_path)
        self.outlook = None
        self.namespace = None

    def _ensure_outlook_running(self) -> bool:
        """Ensure Outlook is running, start it if necessary.
        
        This method checks if Outlook is running and starts it if it's not.
        It uses the Windows command prompt to start Outlook and waits for it
        to initialize before proceeding.
        
        Returns:
            bool: True if Outlook is running, False otherwise
            
        Raises:
            Exception: If there's an error starting Outlook
        """
        import psutil
        
        # Check if Outlook is already running
        outlook_running = any('OUTLOOK.EXE' in (p.name() or '') for p in psutil.process_iter())
        
        if not outlook_running:
            print("Outlook is not running. Attempting to start it...")
            try:
                # Start Outlook using cmd
                outlook_path = settings.OUTLOOK_PATH.replace('/', '\\')  # Convert to Windows path
                cmd = f'cmd /c start "" "{outlook_path}"'
                print(f"Executing command: {cmd}")
                subprocess.run(cmd, shell=True, check=True)
                
                # Wait for Outlook to start (up to 30 seconds)
                for _ in range(30):
                    time.sleep(1)
                    if any('OUTLOOK.EXE' in (p.name() or '') for p in psutil.process_iter()):
                        print("Outlook started successfully!")
                        # Give Outlook a moment to fully initialize
                        time.sleep(5)
                        return True
                
                print("Timed out waiting for Outlook to start")
                return False
                
            except Exception as e:
                print(f"Failed to start Outlook: {str(e)}")
                return False
        
        return True

    def send_email(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Send an email using Outlook.
        
        This method handles the complete email sending process, including:
        - Ensuring Outlook is running
        - Creating a new mail item
        - Setting recipients, subject, and body
        - Adding attachments
        - Sending the email
        - Error handling and logging
        
        Args:
            data: Dictionary containing:
                - to: List of email addresses or single email address
                - subject: Email subject
                - body: Email body
                - cc: Optional list of CC recipients
                - bcc: Optional list of BCC recipients
                - attachments: Optional list of file paths to attach
                
        Returns:
            Dictionary containing:
                - status: "success" or "error"
                - message: Success or error message
                - timestamp: ISO format timestamp
                - details: Additional details about the email (if successful)
                
        Raises:
            Exception: If there's an error during email composition or sending
        """
        try:
            print(f"Initializing Outlook with path: {settings.OUTLOOK_PATH}")
            print(f"Full email data: {data!r}")

            # Ensure Outlook is running
            if not self._ensure_outlook_running():
                return {
                    "status": "error",
                    "message": "Failed to start Outlook. Please start it manually and try again.",
                    "timestamp": datetime.now().isoformat()
                }

            # Initialize Outlook COM objects
            self.outlook = win32com.client.Dispatch("Outlook.Application")
            self.namespace = self.outlook.GetNamespace("MAPI")

            # Create a new mail item
            mail = self.outlook.CreateItem(0)  # 0 represents olMailItem

            # Set recipients
            to_list = data.get('to', [])
            if isinstance(to_list, str):
                to_list = [to_list]
            mail.To = "; ".join(to_list)
            print(f"Set recipients: {to_list}")

            # Set CC if provided
            cc_list = data.get('cc', [])
            if cc_list:
                if isinstance(cc_list, str):
                    cc_list = [cc_list]
                mail.CC = "; ".join(cc_list)
                print(f"Set CC: {cc_list}")

            # Set BCC if provided
            bcc_list = data.get('bcc', [])
            if bcc_list:
                if isinstance(bcc_list, str):
                    bcc_list = [bcc_list]
                mail.BCC = "; ".join(bcc_list)
                print(f"Set BCC: {bcc_list}")

            # Set subject and body
            mail.Subject = data.get('subject', '')
            mail.Body = data.get('body', '')
            print(f"Set subject: {mail.Subject}")

            # Add attachments if provided
            attachments = data.get('attachments', [])
            print(f"Attachments list: {attachments!r}")
            if attachments:
                if isinstance(attachments, str):
                    attachments = [attachments]
                for attachment in attachments:
                    if attachment and attachment.strip():  # Only add if not empty
                        print(f"Adding attachment: {attachment}")
                        if os.path.exists(attachment):
                            mail.Attachments.Add(attachment)
                        else:
                            print(f"Warning: Attachment file not found: {attachment}")

            # Send the email
            print("Sending email...")
            mail.Send()
            print("Email sent successfully!")

            return {
                "status": "success",
                "message": "Email sent successfully",
                "timestamp": datetime.now().isoformat(),
                "details": {
                    "to": to_list,
                    "cc": cc_list,
                    "bcc": bcc_list,
                    "subject": data.get('subject', ''),
                    "attachments": attachments
                }
            }

        except Exception as e:
            error_msg = f"Failed to send email: {str(e)}"
            print(error_msg)
            return {
                "status": "error",
                "message": error_msg,
                "timestamp": datetime.now().isoformat()
            } 