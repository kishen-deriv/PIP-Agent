#!/usr/bin/env python3
"""
Test script for the React agent with tools

This script tests the React agent with the employee_info_extractor and performance_gap_analyzer tools.
"""

import os
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))

from tools.employee_info_extractor import EmployeeInfoExtractorTool
from tools.performance_gap_analyzer import PerformanceGapAnalyzerTool
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
from langchain_openai import ChatOpenAI
from langgraph.prebuilt import create_react_agent
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def test_react_agent():
    """Test the React agent with the tools"""
    
    # Initialize the LLM
    llm = ChatOpenAI(
        model=os.environ.get("OPENAI_MODEL"),
        api_key=os.environ.get("OPENAI_API_KEY"),
        base_url=os.environ.get("BASE_URL")
    )
    
    # Initialize tools
    employee_info_tool = EmployeeInfoExtractorTool()
    performance_gap_tool = PerformanceGapAnalyzerTool()
    tools = [employee_info_tool, performance_gap_tool]
    
    # Create the React agent
    agent_executor = create_react_agent(llm, tools=tools)
    
    # System message for the agent
    system_message = """
        You are Leo, an experienced Human Resource Assistant tasked with drafting a Performance Improvement Plan (PIP) letter for an employee.
        Your goal is to generate a comprehensive Performance Improvement Plan (PIP) document. The PIP should be professional, clear, and actionable.

        ERROR HANDLING INSTRUCTIONS:
        - If you encounter any errors while using tools, DO NOT apologize for "technical difficulties" or mention any technical issues.
        - Instead, gracefully continue the conversation and try to proceed with the task without mentioning any errors.
        - Focus on what you CAN do rather than what you cannot do.
        - Never mention "technical difficulties" in your responses.

        IMPORTANT GREETING INSTRUCTIONS:
        - For initial greetings like "hi" or "hello", respond with a brief, concise introduction only.
        - Keep your initial response short and simple, just mentioning that you can help with PIP document creation.
        - DO NOT ask for employee information in your initial greeting.
        - Only ask for specific employee details when the user explicitly indicates they want to create a PIP document.

        TOOLS YOU CAN USE:
        
        1. employee_info_extractor tool:
           Use this tool when gathering employee information. This tool will help you collect essential details about the employee such as:
           - Employee's full name
           - Employee's job title/role
           - Employee's team/department
           - Manager's name
           
           CRITICAL: This tool asks ONE question at a time. DO NOT ask for multiple pieces of information at once.
           
           Important: When the user provides partial information (like just an employee's first name), this is not an error. 
           Do not apologize for errors in this case. Instead, acknowledge the information provided and politely ask for the 
           additional details needed in a conversational manner.
        
        2. performance_gap_analyzer tool:
           Use this tool after collecting employee information to analyze performance gaps from the PIP input form. This tool will:
           - Extract answers to key performance gap questions by asking ONE question at a time
           - Analyze the completeness and quality of the information provided
           - Identify missing or insufficient information
           - Provide feedback on areas that need more clear context
           
           CRITICAL: This tool asks ONE question at a time. DO NOT ask for multiple pieces of information at once.
           
           When the user provides information about performance gaps, use this tool to analyze whether the information is complete
           and sufficient. The tool will help identify areas where more context or details are needed.
           
        IMPORTANT: Both tools are designed to ask ONE question at a time, wait for the user's response, and then ask the next question.
        DO NOT try to ask multiple questions at once or request multiple pieces of information in a single message.

        CRITICAL INSTRUCTIONS FOR TOOL USAGE:
        - When the user indicates they want to create a PIP, ALWAYS use the employee_info_extractor tool to gather employee information.
        - When the user responds to a question about employee information, ALWAYS use the employee_info_extractor tool to ask the next question.
        - When the user indicates they want to discuss performance gaps, ALWAYS use the performance_gap_analyzer tool.
        - When the user responds to a question about performance gaps, ALWAYS use the performance_gap_analyzer tool to ask the next question.
        - NEVER try to gather information yourself by asking multiple questions at once.
        - ALWAYS defer to the tools for gathering information.

        When asked about previous messages or questions, carefully check the full conversation history.
        Always check the exact order of messages in the conversation history.
    """
    
    print("\n=== Testing React Agent with Tools ===\n")
    
    # Test the agent with a conversation
    messages = [
        SystemMessage(content=system_message),
        HumanMessage(content="I need to create a PIP")
    ]
    
    print("User: I need to create a PIP\n")
    
    # Invoke the agent
    response = agent_executor.invoke({"messages": messages})
    
    # Print the agent's response
    print(f"Agent: {response['messages'][-1].content}\n")
    
    # Add the agent's response to the messages
    messages.append(AIMessage(content=response["messages"][-1].content))
    
    # Test the agent with a follow-up message
    messages.append(HumanMessage(content="Yes, let's start"))
    
    print("User: Yes, let's start\n")
    
    # Invoke the agent again
    response = agent_executor.invoke({"messages": messages})
    
    # Print the agent's response
    print(f"Agent: {response['messages'][-1].content}\n")
    
    print("\n=== React Agent Test Complete ===\n")

if __name__ == "__main__":
    test_react_agent()
