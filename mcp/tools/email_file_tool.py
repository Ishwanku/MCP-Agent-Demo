"""
Email file tool implementation for the MCP Agent.

This module provides functionality to parse and process email files in a specific format.
It handles reading email files, extracting email components, and preparing them for sending.

Key Features:
- Email file parsing with a structured format
- Support for multiple recipients (To, CC, BCC)
- Attachment path handling
- Validation of email components
- Detailed error reporting

File Format:
    The email file should follow this structure:
    ```
    TO: recipient@example.com
    CC: cc@example.com
    BCC: bcc@example.com
    SUBJECT: Your Subject Here
    BODY: Your email body text here.
    ATTACHMENTS:
    path/to/attachment1.pdf
    path/to/attachment2.docx
    ```

Example:
    ```python
    email_file_tool = EmailFileTool()
    result = email_file_tool.process_email_file('path/to/email.txt')
    ```

Dependencies:
    - os: For file path operations
    - datetime: For timestamp generation
"""

import os
from typing import Dict, Any, List, Optional
from datetime import datetime
from mcp.tools.email_tool import EmailTool

class EmailFileTool:
    """A tool for processing email files.
    
    This class provides functionality to read and parse email files in a specific format,
    extracting all necessary components for sending an email.
    
    Attributes:
        None
        
    Methods:
        process_email_file: Process an email file and extract its components
        _parse_email_file: Parse the email file content
        _validate_email_data: Validate the extracted email data
    """

    def __init__(self):
        """Initialize the email file tool."""
        self.email_tool = EmailTool()

    def process_email_file(self, file_path: str) -> Dict[str, Any]:
        """Process an email file and extract its components.
        
        This method reads an email file, parses its contents, and prepares the data
        for sending. It handles all the necessary validation and error checking.
        
        Args:
            file_path: Path to the email file
            
        Returns:
            Dictionary containing:
                - status: "success" or "error"
                - message: Success or error message
                - timestamp: ISO format timestamp
                - data: Extracted email data (if successful)
                
        Raises:
            FileNotFoundError: If the email file doesn't exist
            ValueError: If the email file format is invalid
        """
        try:
            print(f"Processing email file: {file_path}")
            
            # Check if file exists
            if not os.path.exists(file_path):
                return {
                    "status": "error",
                    "message": f"Email file not found: {file_path}",
                    "timestamp": datetime.now().isoformat()
                }
            
            # Parse the email file
            email_data = self._parse_email_file(file_path)
            
            # Validate the email data
            validation_result = self._validate_email_data(email_data)
            if validation_result["status"] == "error":
                return validation_result
            
            return {
                "status": "success",
                "message": "Email file processed successfully",
                "timestamp": datetime.now().isoformat(),
                "data": email_data
            }
            
        except Exception as e:
            error_msg = f"Failed to process email file: {str(e)}"
            print(error_msg)
            return {
                "status": "error",
                "message": error_msg,
                "timestamp": datetime.now().isoformat()
            }

    def _parse_email_file(self, file_path: str) -> Dict[str, Any]:
        """Parse the email file content.
        
        This method reads the email file and extracts all components according to
        the specified format. It handles multiple recipients and attachments.
        
        Args:
            file_path: Path to the email file
            
        Returns:
            Dictionary containing the extracted email components:
                - to: List of primary recipients
                - cc: List of CC recipients
                - bcc: List of BCC recipients
                - subject: Email subject
                - body: Email body
                - attachments: List of attachment paths
                
        Raises:
            ValueError: If the file format is invalid
        """
        email_data = {
            "to": [],
            "cc": [],
            "bcc": [],
            "subject": "",
            "body": "",
            "attachments": []
        }
        
        current_section = None
        body_lines = []
        
        with open(file_path, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                
                # Check for section headers
                if line.upper().startswith(("TO:", "CC:", "BCC:", "SUBJECT:", "BODY:", "ATTACHMENTS:")):
                    current_section = line.split(":", 1)[0].upper()
                    value = line.split(":", 1)[1].strip()
                    
                    if current_section == "TO":
                        email_data["to"] = [addr.strip() for addr in value.split(",")]
                    elif current_section == "CC":
                        email_data["cc"] = [addr.strip() for addr in value.split(",")]
                    elif current_section == "BCC":
                        email_data["bcc"] = [addr.strip() for addr in value.split(",")]
                    elif current_section == "SUBJECT":
                        email_data["subject"] = value
                    elif current_section == "BODY":
                        body_lines.append(value)
                    elif current_section == "ATTACHMENTS":
                        if value:
                            email_data["attachments"].append(value)
                elif current_section == "BODY":
                    body_lines.append(line)
                elif current_section == "ATTACHMENTS":
                    if line:
                        email_data["attachments"].append(line)
        
        email_data["body"] = "\n".join(body_lines)
        return email_data

    def _validate_email_data(self, email_data: Dict[str, Any]) -> Dict[str, Any]:
        """Validate the extracted email data.
        
        This method performs validation checks on the extracted email data to ensure
        all required components are present and properly formatted.
        
        Args:
            email_data: Dictionary containing the extracted email components
            
        Returns:
            Dictionary containing:
                - status: "success" or "error"
                - message: Success or error message
                - timestamp: ISO format timestamp
                
        Raises:
            ValueError: If validation fails
        """
        # Check required fields
        if not email_data["to"]:
            return {
                "status": "error",
                "message": "No recipients specified",
                "timestamp": datetime.now().isoformat()
            }
        
        if not email_data["subject"]:
            return {
                "status": "error",
                "message": "No subject specified",
                "timestamp": datetime.now().isoformat()
            }
        
        if not email_data["body"]:
            return {
                "status": "error",
                "message": "No body specified",
                "timestamp": datetime.now().isoformat()
            }
        
        # Validate email addresses (basic format check)
        for field in ["to", "cc", "bcc"]:
            for email in email_data[field]:
                if "@" not in email or "." not in email:
                    return {
                        "status": "error",
                        "message": f"Invalid email address in {field}: {email}",
                        "timestamp": datetime.now().isoformat()
                    }
        
        # Validate attachments
        for attachment in email_data["attachments"]:
            if not os.path.exists(attachment):
                return {
                    "status": "error",
                    "message": f"Attachment not found: {attachment}",
                    "timestamp": datetime.now().isoformat()
                }
        
        return {
            "status": "success",
            "message": "Email data validated successfully",
            "timestamp": datetime.now().isoformat()
        }

    def send_email_from_file(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Send an email using details from a text file.
        
        Args:
            data: Dictionary containing:
                - file_path: Path to the text file containing email details
                
        Returns:
            Dictionary containing the status of the email sending operation
        """
        try:
            file_path = data.get('file_path')
            if not file_path:
                return {
                    "status": "error",
                    "message": "No file path provided",
                    "timestamp": datetime.now().isoformat()
                }

            # Parse the email file
            email_data = self._parse_email_file(file_path)

            # Validate required fields
            if not email_data['to']:
                return {
                    "status": "error",
                    "message": "No recipients specified in the email file",
                    "timestamp": datetime.now().isoformat()
                }

            if not email_data['subject']:
                return {
                    "status": "error",
                    "message": "No subject specified in the email file",
                    "timestamp": datetime.now().isoformat()
                }

            # Send the email using the email tool
            return self.email_tool.send_email(email_data)

        except FileNotFoundError as e:
            return {
                "status": "error",
                "message": str(e),
                "timestamp": datetime.now().isoformat()
            }
        except ValueError as e:
            return {
                "status": "error",
                "message": str(e),
                "timestamp": datetime.now().isoformat()
            }
        except Exception as e:
            return {
                "status": "error",
                "message": f"Failed to send email: {str(e)}",
                "timestamp": datetime.now().isoformat()
            } 