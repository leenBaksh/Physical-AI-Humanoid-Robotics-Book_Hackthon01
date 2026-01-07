#!/usr/bin/env python3
"""
Fresh test to check what routes are registered in the API
"""

# Clear any cached modules
import sys
modules_to_remove = [key for key in sys.modules.keys() if 'api' in key or 'agent' in key]
for module in modules_to_remove:
    del sys.modules[module]

# Now import fresh
import os
import sys

# Add backend directory to path to access Qdrant storage
backend_path = os.path.join(os.path.dirname(__file__), 'backend')
if backend_path not in sys.path:
    sys.path.insert(0, backend_path)

from api import app

print("Registered routes:")
for route in app.routes:
    print(f"  {route.methods} {route.path}")

print(f"\nTotal routes: {len(app.routes)}")

# Also verify the app object is from the right file
print(f"\nApp object location: {app.__module__ if hasattr(app, '__module__') else 'Unknown'}")