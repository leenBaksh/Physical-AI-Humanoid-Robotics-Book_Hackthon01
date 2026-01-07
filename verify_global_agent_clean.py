#!/usr/bin/env python3
"""
Verify that the global agent is properly initialized (without path manipulation)
"""

from api import app, book_agent

print("Checking global book_agent variable...")
print(f"book_agent value: {book_agent}")
print(f"book_agent type: {type(book_agent)}")

if book_agent is not None:
    print("book_agent is properly initialized!")
else:
    print("book_agent is None - startup event may not have run")

# Check if routes are properly registered
print("\nRegistered routes:")
for route in app.routes:
    if route.path in ['/', '/chat']:
        print(f"  {route.methods} {route.path}")