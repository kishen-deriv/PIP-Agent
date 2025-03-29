#!/usr/bin/env python3
"""
A simple command-line interface for chatting with the agent.
This demonstrates how to use the agent with persistent memory across sessions.
"""

import sys
import os
from pathlib import Path
import argparse

# Add the parent directory to the path so we can import from src
sys.path.append(str(Path(__file__).parent.parent))

from src.agent import chat_with_memory, MEMORY_FILE
import json
import shutil

def clear_thread_memory(thread_id=None):
    """Clear memory for a specific thread or all threads"""
    if MEMORY_FILE.exists():
        if thread_id:
            # Clear only the specified thread
            try:
                with open(MEMORY_FILE, 'r') as f:
                    all_memory = json.load(f)
                
                if thread_id in all_memory:
                    del all_memory[thread_id]
                    
                    with open(MEMORY_FILE, 'w') as f:
                        json.dump(all_memory, f, indent=2)
                    
                    print(f"Cleared conversation history for thread: {thread_id}")
                else:
                    print(f"No conversation history found for thread: {thread_id}")
            except Exception as e:
                print(f"Error clearing memory: {e}")
        else:
            # Clear all threads
            os.remove(MEMORY_FILE)
            print("Cleared all conversation history")

def main():
    """Main function for the CLI chat application"""
    parser = argparse.ArgumentParser(description="Chat with an AI agent with persistent memory")
    parser.add_argument("--thread", "-t", default="default", help="Thread ID for the conversation (default: 'default')")
    parser.add_argument("--clear", "-c", action="store_true", help="Clear the conversation history before starting")
    parser.add_argument("--list", "-l", action="store_true", help="List all available conversation threads")
    args = parser.parse_args()
    
    thread_id = args.thread
    
    # List all available threads if requested
    if args.list:
        if MEMORY_FILE.exists():
            try:
                with open(MEMORY_FILE, 'r') as f:
                    all_memory = json.load(f)
                
                if all_memory:
                    print("Available conversation threads:")
                    for tid in all_memory.keys():
                        msg_count = len(all_memory[tid].get("messages", []))
                        print(f"  - {tid} ({msg_count} messages)")
                else:
                    print("No conversation threads found")
            except Exception as e:
                print(f"Error listing threads: {e}")
        else:
            print("No conversation history found")
        return
    
    # Clear conversation history if requested
    if args.clear:
        clear_thread_memory(thread_id)
    
    print(f"Starting chat session with thread ID: {thread_id}")
    print("Type 'exit', 'quit', or press Ctrl+C to end the conversation")
    print("Type '!clear' to clear the current conversation history")
    print("Type '!help' for more commands")
    print("-" * 50)
    
    try:
        while True:
            user_input = input("\nYou: ")
            
            # Handle special commands
            if user_input.lower() in ["exit", "quit"]:
                print("Goodbye!")
                break
            elif user_input.lower() == "!help":
                print("\nAvailable commands:")
                print("  !clear       - Clear the current conversation history")
                print("  !list        - List all messages in the current thread")
                print("  !switch NAME - Switch to a different conversation thread")
                print("  !help        - Show this help message")
                print("  exit, quit   - Exit the application")
                continue
            elif user_input.lower() == "!clear":
                clear_thread_memory(thread_id)
                continue
            elif user_input.lower() == "!list":
                if MEMORY_FILE.exists():
                    try:
                        with open(MEMORY_FILE, 'r') as f:
                            all_memory = json.load(f)
                        
                        if thread_id in all_memory:
                            messages = all_memory[thread_id].get("messages", [])
                            if messages:
                                print(f"\nMessages in thread '{thread_id}':")
                                for i, msg in enumerate(messages):
                                    role = msg.get("role", "unknown")
                                    content = msg.get("content", "")
                                    print(f"{i+1}. [{role.upper()}] {content[:50]}{'...' if len(content) > 50 else ''}")
                            else:
                                print(f"No messages in thread '{thread_id}'")
                        else:
                            print(f"Thread '{thread_id}' not found")
                    except Exception as e:
                        print(f"Error listing messages: {e}")
                else:
                    print("No conversation history found")
                continue
            elif user_input.lower().startswith("!switch "):
                new_thread = user_input[8:].strip()
                if new_thread:
                    thread_id = new_thread
                    print(f"Switched to thread: {thread_id}")
                else:
                    print("Please specify a thread name")
                continue
            
            # Normal chat interaction
            response = chat_with_memory(user_input, thread_id=thread_id)
            print(f"\nAI: {response}")
    
    except KeyboardInterrupt:
        print("\nGoodbye!")
        sys.exit(0)

if __name__ == "__main__":
    main()
