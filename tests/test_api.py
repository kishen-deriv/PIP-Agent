#!/usr/bin/env python3
"""
A simple script to test the API connection.
"""

import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage

# Load environment variables
load_dotenv()

def get_env_var(key):
    """Get environment variable or raise an error if not found"""
    value = os.getenv(key)
    if value is None:
        raise ValueError(f"Environment variable {key} not found")
    return value

def test_api():
    """Test the API connection"""
    try:
        # Get environment variables
        model_name = get_env_var("ANTHROPIC_MODEL")
        api_key = get_env_var("ANTHROPIC_API_KEY")
        base_url = get_env_var("BASE_URL")
        
        print(f"Using model: {model_name}")
        print(f"Using base URL: {base_url}")
        
        # Initialize the model
        model = ChatOpenAI(
            model=model_name,
            api_key=api_key,
            base_url=base_url
        )
        
        # Create a simple message
        messages = [HumanMessage(content="Hello, how are you?")]
        
        # Invoke the model
        print("Sending request to API...")
        response = model.invoke(messages)
        
        # Print the response
        print("\nResponse:")
        print(response.content)
        
        return True
    except Exception as e:
        import traceback
        print(f"Error: {e}")
        print(f"Detailed error: {traceback.format_exc()}")
        return False

if __name__ == "__main__":
    print("Testing API connection...")
    success = test_api()
    if success:
        print("\nAPI test successful!")
    else:
        print("\nAPI test failed.")
