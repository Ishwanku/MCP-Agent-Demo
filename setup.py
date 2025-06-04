"""
Setup script for the MCP Agent Demo package.

This is a minimal setup.py that works with both modern (pyproject.toml) and legacy
setuptools installations. The main package configuration is in pyproject.toml.
"""

from setuptools import setup

setup(
    name="mcp-agent-demo",
    packages=["mcp"],
    package_dir={"mcp": "mcp"},
    python_requires=">=3.9",
    install_requires=[
        "fastapi>=0.92.0",
        "uvicorn>=0.20.0",
        "pydantic>=2.0.0",
        "python-dotenv>=1.0.0",
        "pydantic-settings>=2.0.0",
    ],
) 