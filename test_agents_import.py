#!/usr/bin/env python3
"""
Test to check if the agents import is causing the issue
"""

import sys
import os

# Check if the issue is with importing the agents library
print("Testing import of agents library...")

try:
    from agents import Agent, Runner, function_tool, OpenAIChatCompletionsModel
    print("Successfully imported agents library")
except ImportError as e:
    print(f"Failed to import agents library: {e}")

print("Testing import of FastAPI after agents...")

try:
    from fastapi import FastAPI
    print("Successfully imported FastAPI")

    app = FastAPI()
    print(f"Successfully created FastAPI app: {app}")

except Exception as e:
    print(f"Failed to import or create FastAPI app: {e}")
    import traceback
    traceback.print_exc()

print("Testing FastAPI middleware configuration...")

try:
    from fastapi.middleware.cors import CORSMiddleware

    app_with_middleware = FastAPI()
    app_with_middleware.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    print("Successfully added CORS middleware")

except Exception as e:
    print(f"Failed to add CORS middleware: {e}")
    import traceback
    traceback.print_exc()