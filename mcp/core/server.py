"""
Base server implementation for the Demo MCP Agent.

This module provides a FastAPI-based server implementation that can be used
by the demo MCP agent to expose tools and handle requests.
"""

from typing import Any, Callable, Dict
from fastapi import FastAPI, HTTPException, Request
import uvicorn

class FastMCP:
    """A server implementation for the Demo MCP Agent providing tool execution endpoints."""

    def __init__(self, name: str, port: int, api_key: str, tools: Dict[str, Callable] = None):
        """Initialize the FastMCP server.

        Args:
            name (str): Name of the server/agent.
            port (int): Port to run the server on.
            api_key (str): API key for authentication.
            tools (Dict[str, Callable], optional): Dictionary of tool names to their callable functions.
        """
        self.name = name
        self.port = port
        self.api_key = api_key
        self.tools = tools or {}
        self.app = FastAPI(title=f"Demo MCP Agent - {name}")
        self._setup_routes()

    def _setup_routes(self) -> None:
        """Set up the FastAPI routes for tool execution."""
        @self.app.post("/tools/{tool_name}")
        async def execute_tool(tool_name: str, request: Request, data: Dict[str, Any]):
            """Execute a specific tool with the provided data."""
            if request.headers.get("X-API-Key") != self.api_key:
                raise HTTPException(status_code=401, detail="Invalid API key")
            
            if tool_name not in self.tools:
                raise HTTPException(status_code=404, detail=f"Tool {tool_name} not found")
            
            try:
                result = self.tools[tool_name](data)
                return {"status": "success", "data": result}
            except Exception as e:
                raise HTTPException(
                    status_code=500,
                    detail=f"Error executing tool {tool_name}: {str(e)}"
                )

        @self.app.get("/health")
        async def health_check():
            """Health check endpoint."""
            return {"status": "healthy", "agent": self.name}

    def register_tool(self, name: str, func: Callable) -> None:
        """Register a new tool with the server.

        Args:
            name (str): Name of the tool.
            func (Callable): Function to execute for the tool.
        """
        self.tools[name] = func
        print(f"Registered tool '{name}' for {self.name}")

    def run(self) -> None:
        """Run the FastMCP server using Uvicorn."""
        print(f"Starting {self.name} server on port {self.port}")
        uvicorn.run(self.app, host="0.0.0.0", port=self.port, log_level="info") 