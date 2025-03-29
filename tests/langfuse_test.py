#!/usr/bin/env python3
"""
Simple test script to check the available methods in the Langfuse object.
"""

import os
from dotenv import load_dotenv
from langfuse import Langfuse

# Load environment variables
load_dotenv()

# Initialize Langfuse
langfuse = Langfuse(
    secret_key=os.getenv("LANGFUSE_SECRET_KEY"),
    public_key=os.getenv("LANGFUSE_PUBLIC_KEY"),
    host=os.getenv("LANGFUSE_HOST")
)

# Print all available methods and attributes
print("Available methods and attributes in Langfuse object:")
for attr in dir(langfuse):
    if not attr.startswith('_'):  # Skip private attributes
        print(f"- {attr}")

# Try to create a trace
print("\nTrying to create a trace...")
try:
    # Try different methods that might be used to create a trace
    methods_to_try = ["trace", "create_trace", "new_trace", "start_trace"]
    
    for method_name in methods_to_try:
        if hasattr(langfuse, method_name):
            method = getattr(langfuse, method_name)
            print(f"Found method: {method_name}")
            trace = method(name="test_trace")
            print(f"Created trace with ID: {trace.id}")
            
            # Check trace methods
            print(f"\nAvailable methods and attributes in trace object:")
            for attr in dir(trace):
                if not attr.startswith('_'):  # Skip private attributes
                    print(f"- {attr}")
            
            break
    else:
        print("Could not find a method to create a trace")
except Exception as e:
    print(f"Error creating trace: {str(e)}")

print("\nTest completed!")
