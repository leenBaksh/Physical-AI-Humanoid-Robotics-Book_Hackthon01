#!/usr/bin/env python3
"""
Check what routes are registered in the API
"""

import os
import sys

# Add backend directory to path to access Qdrant storage
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))

# Import the API app
from api import app

print("Registered routes:")
for route in app.routes:
    print(f"  {route.methods} {route.path}")

print(f"\nTotal routes: {len(app.routes)}")