import sys
from pathlib import Path
import os
import json
import shutil

# Add the parent directory to the path so we can import from src
sys.path.append(str(Path(__file__).parent.parent))

from src.agent import chat_with_memory, MEMORY_DIR, MEMORY_FILE

def clear_memory():
    """Clear any existing memory files"""
    if MEMORY_FILE.exists():
        os.remove(MEMORY_FILE)
    if MEMORY_DIR.exists() and not os.listdir(MEMORY_DIR):
        shutil.rmtree(MEMORY_DIR)
        MEMORY_DIR.mkdir(exist_ok=True)

def test_conversation_memory():
    """Test that conversation memory persists between function calls"""
    # Clear any existing memory
    clear_memory()
    
    # First interaction
    print("First interaction:")
    response1 = chat_with_memory("Hello, my name is John.")
    print(f"AI: {response1}")
    
    # Second interaction - should remember the name
    print("\nSecond interaction:")
    response2 = chat_with_memory("What's my name?")
    print(f"AI: {response2}")
    
    # Third interaction - ask something else
    print("\nThird interaction:")
    response3 = chat_with_memory("What's 2+2?")
    print(f"AI: {response3}")
    
    # Fourth interaction - should remember previous questions
    print("\nFourth interaction:")
    response4 = chat_with_memory("What was my previous question?")
    print(f"AI: {response4}")
    
    # Check if the agent remembers the name and the most recent question
    name_remembered = "John" in response2
    correct_question_remembered = "2+2" in response4
    
    print(f"\nName remembered: {name_remembered}")
    print(f"Correct previous question remembered: {correct_question_remembered}")
    
    # Print the memory file contents for debugging
    if MEMORY_FILE.exists():
        with open(MEMORY_FILE, 'r') as f:
            memory_content = json.load(f)
            print("\nMemory file contents:")
            print(json.dumps(memory_content, indent=2))
    
    return name_remembered and correct_question_remembered

if __name__ == "__main__":
    result = test_conversation_memory()
    print(f"\nTest passed: {result}")
