"""
FastAPI-based MCP server implementation.

This module provides a FastAPI-based server implementation for the MCP (Multi-Component Protocol)
agent system. It handles tool registration, execution, and API key authentication.

Key Features:
- FastAPI-based REST API
- Tool registration and management
- API key authentication
- Health check endpoint
- Detailed error handling
- Request validation

Example:
    ```python
    server = FastMCP("DemoAgent", port=8000, api_key="secret-key")
    server.register_tool("echo", echo_tool)
    server.run()
    ```

Dependencies:
    - fastapi: For the web server
    - uvicorn: For ASGI server
    - pydantic: For request/response models
"""

from fastapi import FastAPI, HTTPException, Depends, Header
from typing import Dict, Any, Callable, Optional
import uvicorn
from pydantic import BaseModel

class ToolRequest(BaseModel):
    """Request model for tool execution.
    
    This model defines the structure of requests to tool execution endpoints.
    It includes a data field that can contain any JSON-serializable data.
    
    Attributes:
        data: Dictionary containing the tool's input data
    """
    data: Dict[str, Any]

class FastMCP:
    """FastAPI-based MCP server implementation.
    
    This class provides a FastAPI-based server for the MCP agent system.
    It handles tool registration, execution, and API key authentication.
    
    Attributes:
        name: Name of the agent
        port: Port to run the server on
        api_key: Optional API key for authentication
        tools: Dictionary of registered tools
        app: FastAPI application instance
        
    Methods:
        __init__: Initialize the server
        register_tool: Register a tool with the server
        run: Start the server
    """
    
    def __init__(self, name: str, port: int = 8000, api_key: Optional[str] = None):
        """Initialize the FastMCP server.
        
        Args:
            name: Name of the agent
            port: Port to run the server on
            api_key: Optional API key for authentication
        """
        self.name = name
        self.port = port
        self.api_key = api_key
        self.tools: Dict[str, Callable] = {}
        
        # Create FastAPI app
        self.app = FastAPI(title=f"{name} MCP Server")
        
        # Add health check endpoint
        @self.app.get("/health")
        async def health_check():
            """Health check endpoint.
            
            Returns:
                Dictionary containing server status and agent name
            """
            return {"status": "healthy", "agent": name}
        
        # Add tool execution endpoint
        @self.app.post("/tools/{tool_name}")
        async def execute_tool(
            tool_name: str,
            request: ToolRequest,
            api_key: Optional[str] = Header(None, alias="API-Key")
        ):
            """Tool execution endpoint.
            
            This endpoint executes a registered tool with the provided data.
            It includes API key authentication if configured.
            
            Args:
                tool_name: Name of the tool to execute
                request: Tool execution request
                api_key: Optional API key from header
                
            Returns:
                Tool execution result
                
            Raises:
                HTTPException: If authentication fails or tool not found
            """
            # Check API key if configured
            if self.api_key and api_key != self.api_key:
                raise HTTPException(status_code=401, detail="Invalid API key")
            
            # Check if tool exists
            if tool_name not in self.tools:
                raise HTTPException(status_code=404, detail=f"Tool {tool_name} not found")
            
            # Execute tool
            try:
                result = self.tools[tool_name](request.data)
                return result
            except Exception as e:
                raise HTTPException(status_code=500, detail=str(e))
    
    def register_tool(self, name: str, func: Callable) -> None:
        """Register a tool with the server.
        
        This method registers a tool function with the server, making it available
        through the API.
        
        Args:
            name: Name of the tool
            func: Tool function to register
            
        Raises:
            ValueError: If tool name is already registered
        """
        if name in self.tools:
            raise ValueError(f"Tool '{name}' is already registered")
        
        self.tools[name] = func
        print(f"Registered tool '{name}' for {self.name}")
    
    def run(self) -> None:
        """Run the FastAPI server.
        
        This method starts the FastAPI server on the configured port.
        It uses uvicorn as the ASGI server.
        """
        print(f"Starting {self.name} server on port {self.port}")
        uvicorn.run(self.app, host="0.0.0.0", port=self.port) 