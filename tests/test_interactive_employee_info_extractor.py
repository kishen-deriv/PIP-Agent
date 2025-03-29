"""
Test script for the interactive Employee Info Extractor tool

This script simulates how the agent would use the employee_info_extractor tool
with conversation history.
"""

import os
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))

from tools.employee_info_extractor import EmployeeInfoExtractorTool
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def test_interactive_employee_info_extractor():
    """Test the interactive employee info extractor tool with a simulated conversation history"""
    
    # Initialize the tool and LLM
    employee_info_tool = EmployeeInfoExtractorTool()
    llm = ChatOpenAI(
        model=os.environ.get("OPENAI_MODEL"),
        api_key=os.environ.get("OPENAI_API_KEY"),
        base_url=os.environ.get("BASE_URL")
    )
    
    # Simulate a conversation history
    conversation_history = []
    
    # System message for the employee info extractor
    system_message = """
        You are Leo, an HR assistant specialized in gathering employee information.
        Your task is to analyze the conversation history and determine what basic employee information you still need to collect.

        You need to collect:
        1. Employee's full name
        2. Employee's job title/role
        3. Employee's team/department (if applicable)
        4. Manager's name

        Important guidelines:
        - Ask only ONE question at a time
        - Wait for the user's response before asking the next question
        - Keep track of which information you've already collected and which you still need
        - When the user provides partial information (like just an employee's first name), this is not an error
        - Do not apologize for errors in this case. Instead, acknowledge the information provided and politely ask for the
          additional details needed in a conversational manner

        IMPORTANT: You must carefully analyze the conversation history to determine:
        1. What employee information has already been collected
        2. What information still needs to be gathered
        
        DO NOT ask for information that has already been provided. Use the conversation history to maintain context.
        
        The conversation should follow this general flow:
        1. Ask for the employee's full name
        2. Ask for the employee's job title/role
        3. Ask for the employee's team/department (if applicable)
        4. Ask for the manager's name
        5. Once all information is collected, summarize what you've gathered
        
        NEVER ask multiple questions at once. Ask ONE question, wait for the response, then ask the next question.
        
        Be conversational and professional. Focus ONLY on gathering the basic employee information listed above, not performance details or improvement plans.
    """
    
    print("\n=== Starting Employee Information Gathering ===\n")
    
    # Start the conversation
    user_input = "I need to create a PIP for an employee."
    print(f"User: {user_input}\n")
    
    # Add to conversation history
    conversation_history.append(HumanMessage(content=user_input))
    
    # Get the first question from the tool
    messages = [SystemMessage(content=system_message)] + conversation_history
    response = llm.invoke(messages)
    print(f"Tool: {response.content}\n")
    
    # Add to conversation history
    conversation_history.append(AIMessage(content=response.content))
    
    # Simulate user responses for employee information
    user_responses = [
        "The employee's name is John Smith",
        "He is a Senior Software Engineer",
        "He works in the Engineering department, specifically on the Backend team",
        "His manager is Sarah Johnson"
    ]
    
    # Process each user response and get the next question
    for i, user_response in enumerate(user_responses):
        print(f"User: {user_response}\n")
        
        # Add to conversation history
        conversation_history.append(HumanMessage(content=user_response))
        
        # Get the next question from the tool
        messages = [SystemMessage(content=system_message)] + conversation_history
        response = llm.invoke(messages)
        print(f"Tool: {response.content}\n")
        
        # Add to conversation history
        conversation_history.append(AIMessage(content=response.content))
    
    print("\n=== Employee Information Gathering Complete ===\n")
    
    return response.content

if __name__ == "__main__":
    test_interactive_employee_info_extractor()
