"""
Employee Information Extractor Tool

This tool uses the LLM to dynamically gather basic employee information through conversation.
"""

from langchain.tools import BaseTool
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
import os
from typing import Optional, Type, Dict, Any, List
from pydantic import BaseModel, Field

class EmployeeInfoExtractorTool(BaseTool):
    """Tool that dynamically gathers basic employee information through conversation."""
    name: str = "employee_info_extractor"
    description: str = """
    Use this tool when you need to gather basic employee information.
    This tool will help collect essential details about the employee such as:
    - Employee's job title/role
    - Employee's team/department
    """
    
    def _run(self, input_text: str = "") -> str:
        """Run the employee info gathering process."""
        # Initialize the LLM
        llm = ChatOpenAI(
            model=os.environ.get("ANTHROPIC_MODEL"),
            api_key=os.environ.get("API_KEY"),
            base_url=os.environ.get("BASE_URL")
        )
        
        # Create a system message that instructs the LLM how to gather employee information
        system_message = """
            You are Leo, an HR assistant specialized in gathering employee information.
            
            CRITICAL INSTRUCTION: You must ask ONLY ONE QUESTION at a time. This is the most important rule.
            
            Your task is to analyze the conversation history and determine what basic employee information you still need to collect.

            You need to collect:
            1. Employee's job title/role
            2. Employee's team/department (if applicable)

            Important guidelines:
            - Ask ONLY ONE QUESTION at a time - NEVER combine multiple questions
            - NEVER ask for multiple pieces of information in a single question
            - After each user input, analyze the input and provide immediate feedback
            - If the input is incomplete or unclear, provide specific feedback on what additional information is needed
            - After providing feedback, ask if the user wants to refine their input
            - If the user is satisfied with their input, proceed to the next question
            - Keep track of which information you've already collected and which you still need
            - When the user provides partial information (like just an employee's first name), this is not an error
            - Do not apologize for errors in this case. Instead, acknowledge the information provided and politely ask for the
              additional details needed in a conversational manner

            IMPORTANT: You must carefully analyze the conversation history to determine:
            1. What employee information has already been collected
            2. What information still needs to be gathered
            
            DO NOT ask for information that has already been provided. Use the conversation history to maintain context.
            
            The conversation MUST follow this exact flow:
            1. First question: "What is the employee's job title or role?"
               - After user input, Provide brief feedback without asking for additional details that will be covered in future questions
               - Ask if they want to refine it or move to the next question
            2. Second question: "What team or department does the employee work in?"
               - After user input, Provide brief feedback without asking for additional details that will be covered in future questions
               - Ask if they want to refine it or move to the next question
            
            CRITICAL: NEVER ask multiple questions at once. Ask ONE question, wait for the response, then ask the next question.
            NEVER ask for multiple pieces of information in a single question.
            NEVER use bullet points to list multiple questions.
            
            Be conversational and professional. Focus ONLY on gathering the basic employee information listed above, not performance details or improvement plans.
        """
        
        # Create messages for the LLM
        messages = [
            SystemMessage(content=system_message),
            HumanMessage(content=f"Based on this conversation, what employee information should I ask for next?\n\n{input_text}")
        ]
        
        # Get the next question or summary from the LLM
        response = llm.invoke(messages)
        
        return response.content
    
    def _arun(self, input_text: str = "") -> str:
        """Run the employee info gathering process asynchronously."""
        raise NotImplementedError("Async version not implemented")
