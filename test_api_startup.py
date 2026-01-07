#!/usr/bin/env python3
"""
Test script to test API startup with BookAgent
"""

import asyncio
import sys
import os

# Add backend directory to path to access Qdrant storage
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))

print("Importing api module...")
try:
    import api
    print("API module imported successfully")

    # Try to access the app directly
    print(f"App object: {api.app}")
    print(f"App routes: {[route.path for route in api.app.routes]}")

except Exception as e:
    print(f"Error importing API module: {e}")
    import traceback
    traceback.print_exc()