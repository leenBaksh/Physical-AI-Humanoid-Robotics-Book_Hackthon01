#!/usr/bin/env python3
"""
Find where the agents module is being imported from
"""

import sys

print("Python path:")
for path in sys.path:
    print(f"  {path}")

print("\nTrying to import agents and find its location...")

try:
    import agents
    print(f"Agents module found at: {agents.__file__}")
    print(f"Agents module type: {type(agents)}")
    print(f"Agents module attributes: {dir(agents)}")
except ImportError as e:
    print(f"Could not import agents: {e}")

    # Try to find any agents-related modules
    import importlib.util
    import os

    print("\nSearching for agents module in common locations...")

    for path in sys.path:
        if path:  # Skip empty paths
            agents_path_py = os.path.join(path, 'agents.py')
            agents_path_dir = os.path.join(path, 'agents')

            if os.path.exists(agents_path_py):
                print(f"Found agents.py at: {agents_path_py}")

            if os.path.exists(agents_path_dir) and os.path.isdir(agents_path_dir):
                print(f"Found agents directory at: {agents_path_dir}")

except Exception as e:
    print(f"Error during search: {e}")