"""
Demo MCP Agent implementation.

This module provides a simple example of how to create an MCP agent
with multiple tools and demonstrate the core functionality.
"""

from typing import Dict, Any, List, Optional
from datetime import datetime
import json
import re
from mcp.core.server import FastMCP
from mcp.core.config import settings
from mcp.tools.email_tool import EmailTool
from mcp.tools.email_file_tool import EmailFileTool

class DemoAgent:
    """A demo MCP agent that showcases basic functionality."""

    def __init__(self):
        """Initialize the demo agent with its tools."""
        self.server = FastMCP(
            name="Demo Agent",
            port=settings.DEMO_AGENT_PORT,
            api_key=settings.DEMO_AGENT_API_KEY
        )
        
        # Initialize email tools
        self.email_tool = EmailTool()
        self.email_file_tool = EmailFileTool()
        
        # Register demo tools
        self.server.register_tool('echo', self.echo)
        self.server.register_tool('calculate', self.calculate)
        self.server.register_tool('analyze_text', self.analyze_text)
        self.server.register_tool('format_json', self.format_json)
        self.server.register_tool('extract_info', self.extract_info)
        self.server.register_tool('validate_data', self.validate_data)
        self.server.register_tool('transform_data', self.transform_data)
        self.server.register_tool('send_email', self.email_tool.send_email)
        self.server.register_tool('send_email_from_file', self.email_file_tool.send_email_from_file)
    
    def echo(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Echo back the input data with timestamp.
        
        Args:
            data: Input data to echo back
            
        Returns:
            Dictionary containing the echoed data and timestamp
        """
        return {
            "echo": data,
            "timestamp": datetime.now().isoformat(),
            "status": "success"
        }
    
    def calculate(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Perform a simple calculation.
        
        Args:
            data: Dictionary containing:
                - operation: One of 'add', 'subtract', 'multiply', 'divide', 'power', 'sqrt'
                - a: First number
                - b: Second number (optional for sqrt)
                
        Returns:
            Dictionary containing the result and operation details
        """
        operation = data.get('operation', 'add')
        a = float(data.get('a', 0))
        b = float(data.get('b', 0))
        
        operations = {
            'add': lambda x, y: x + y,
            'subtract': lambda x, y: x - y,
            'multiply': lambda x, y: x * y,
            'divide': lambda x, y: x / y if y != 0 else "Cannot divide by zero",
            'power': lambda x, y: x ** y,
            'sqrt': lambda x, _: x ** 0.5 if x >= 0 else "Cannot calculate square root of negative number"
        }
        
        if operation not in operations:
            return {
                "status": "error",
                "error": f"Invalid operation: {operation}. Supported operations: {', '.join(operations.keys())}"
            }
        
        try:
            result = operations[operation](a, b)
            return {
                "status": "success",
                "operation": operation,
                "a": a,
                "b": b,
                "result": result
            }
        except Exception as e:
            return {
                "status": "error",
                "error": str(e)
            }
    
    def analyze_text(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze text and return detailed statistics.
        
        Args:
            data: Dictionary containing:
                - text: The text to analyze
                
        Returns:
            Dictionary containing detailed text statistics
        """
        text = data.get('text', '')
        
        # Basic text analysis
        words = text.split()
        sentences = [s.strip() for s in text.split('.') if s.strip()]
        paragraphs = [p.strip() for p in text.split('\n') if p.strip()]
        
        # Count unique words
        unique_words = set(word.lower() for word in words)
        
        # Find longest word
        longest_word = max(words, key=len) if words else ""
        
        return {
            "status": "success",
            "statistics": {
                "character_count": len(text),
                "word_count": len(words),
                "unique_word_count": len(unique_words),
                "sentence_count": len(sentences),
                "paragraph_count": len(paragraphs),
                "average_word_length": sum(len(word) for word in words) / len(words) if words else 0,
                "average_sentence_length": sum(len(s) for s in sentences) / len(sentences) if sentences else 0,
                "longest_word": longest_word,
                "longest_word_length": len(longest_word)
            }
        }
    
    def format_json(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Format and validate JSON data.
        
        Args:
            data: Dictionary containing:
                - json_string: The JSON string to format
                - indent: Optional indentation level (default: 2)
                
        Returns:
            Dictionary containing the formatted JSON
        """
        json_string = data.get('json_string', '{}')
        indent = int(data.get('indent', 2))
        
        try:
            # Parse and validate JSON
            parsed = json.loads(json_string)
            # Format JSON with specified indentation
            formatted = json.dumps(parsed, indent=indent)
            return {
                "status": "success",
                "formatted_json": formatted,
                "is_valid": True
            }
        except json.JSONDecodeError as e:
            return {
                "status": "error",
                "error": f"Invalid JSON: {str(e)}",
                "is_valid": False
            }
    
    def extract_info(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Extract specific information from text using patterns.
        
        Args:
            data: Dictionary containing:
                - text: The text to analyze
                - patterns: Dictionary of pattern names to regex patterns
                
        Returns:
            Dictionary containing extracted information
        """
        text = data.get('text', '')
        patterns = data.get('patterns', {
            'email': r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b',
            'phone': r'\b\d{3}[-.]?\d{3}[-.]?\d{4}\b',
            'url': r'https?://(?:[-\w.]|(?:%[\da-fA-F]{2}))+'
        })
        
        results = {}
        for name, pattern in patterns.items():
            matches = re.findall(pattern, text)
            results[name] = matches
        
        return {
            "status": "success",
            "extracted_info": results
        }
    
    def validate_data(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Validate data against specified rules.
        
        Args:
            data: Dictionary containing:
                - data: The data to validate
                - rules: Dictionary of validation rules
                
        Returns:
            Dictionary containing validation results
        """
        data_to_validate = data.get('data', {})
        rules = data.get('rules', {})
        
        results = {
            "is_valid": True,
            "errors": []
        }
        
        for field, rule in rules.items():
            value = data_to_validate.get(field)
            
            if 'required' in rule and rule['required'] and value is None:
                results["is_valid"] = False
                results["errors"].append(f"{field} is required")
            
            if value is not None:
                if 'type' in rule and not isinstance(value, eval(rule['type'])):
                    results["is_valid"] = False
                    results["errors"].append(f"{field} must be of type {rule['type']}")
                
                if 'min_length' in rule and len(str(value)) < rule['min_length']:
                    results["is_valid"] = False
                    results["errors"].append(f"{field} must be at least {rule['min_length']} characters")
                
                if 'max_length' in rule and len(str(value)) > rule['max_length']:
                    results["is_valid"] = False
                    results["errors"].append(f"{field} must be at most {rule['max_length']} characters")
        
        return {
            "status": "success",
            "validation_results": results
        }
    
    def transform_data(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Transform data according to specified rules.
        
        Args:
            data: Dictionary containing:
                - data: The data to transform
                - transformations: List of transformation rules
                
        Returns:
            Dictionary containing transformed data
        """
        data_to_transform = data.get('data', {})
        transformations = data.get('transformations', [])
        
        result = data_to_transform.copy()
        
        for transform in transformations:
            operation = transform.get('operation')
            field = transform.get('field')
            value = transform.get('value')
            
            if operation == 'set':
                result[field] = value
            elif operation == 'delete':
                result.pop(field, None)
            elif operation == 'rename':
                new_field = transform.get('new_field')
                if field in result:
                    result[new_field] = result.pop(field)
            elif operation == 'convert':
                if field in result:
                    try:
                        result[field] = eval(f"{transform.get('type')}({result[field]})")
                    except Exception as e:
                        return {
                            "status": "error",
                            "error": f"Conversion error for field {field}: {str(e)}"
                        }
        
        return {
            "status": "success",
            "transformed_data": result
        }
    
    def run(self) -> None:
        """Run the demo agent server."""
        self.server.run()

if __name__ == "__main__":
    agent = DemoAgent()
    agent.run() 