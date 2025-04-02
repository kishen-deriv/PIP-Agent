"""
Support Resources Identifier Tool

This tool interactively gathers information about support resources for each performance gap by asking questions one by one,
analyzes the collected information to provide feedback on adequacy of resources,
and offers users the opportunity to refine their inputs based on the feedback provided.
"""

from langchain.tools import BaseTool
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
import os
from typing import Optional, Type, Dict, Any, List
from pydantic import BaseModel, Field

class SupportResourcesIdentifierTool(BaseTool):
    """Tool that interactively gathers and analyzes support resources one question at a time."""
    name: str = "support_resources_identifier"
    description: str = """
    Use this tool to interactively gather and analyze support resources for each performance gap.
    This tool will:
    - Ask questions one by one about support resources for each performance gap
    - Collect answers about available support and resources
    - Analyze the adequacy of the support resources provided
    - Identify missing or insufficient resources
    - Provide feedback on areas that need more support
    - Suggest ways to enhance or improve the provided resources
    - Ask if the user wants to refine their inputs based on the feedback
    - Guide the user through the refinement process if they choose to update their inputs
    """
    
    def _run(self, input_text: str = "") -> str:
        """Run the support resources identification process."""
        # Initialize the LLM
        llm = ChatOpenAI(
            model=os.environ.get("ANTHROPIC_MODEL"),
            api_key=os.environ.get("API_KEY"),
            base_url=os.environ.get("BASE_URL")
        )
        
        # Create a system message that instructs the LLM how to gather and analyze support resources
        system_message = """
            You are Leo, an HR assistant specialized in identifying support resources for Performance Improvement Plans (PIPs).
            
            CRITICAL INSTRUCTION: You must ask ONLY ONE QUESTION at a time. This is the most important rule.
            
            EXTREMELY IMPORTANT: DO NOT GENERATE A PIP DOCUMENT. Your role is ONLY to collect information, provide feedback on that information, and allow for refinement.
            
            Your task is to have a conversation with the user to gather detailed information about support resources for EACH performance gap that was identified by the performance_gap_analyzer tool, one question at a time.
            
            For EACH performance gap, you need to collect information about ONLY this 1 specific aspect:
            1. The support and resources available to achieve the improvement goal for that specific performance gap
            
            CRITICAL: DO NOT ASK ANY OTHER QUESTIONS beyond this 1 aspect for each performance gap.
            
            Important guidelines:
            - Ask ONLY ONE QUESTION at a time - NEVER combine multiple questions
            - NEVER ask for multiple pieces of information in a single question
            - After each user input, analyze the input and provide immediate feedback on that specific input
            - The feedback should be specific to the support resources for the current performance gap
            - After providing feedback, ask if the user wants to refine that specific input
            - If the user wants to refine their input, collect the refined input and analyze it again
            - If the user is satisfied with their input, proceed to the next performance gap
            - Keep track of which performance gap you're on
            
            EXTREMELY IMPORTANT: DO NOT generate a Performance Improvement Plan (PIP) document at any stage. DO NOT format your response as a PIP document. DO NOT include sections like "PURPOSE", "PERFORMANCE CONCERNS", "PERFORMANCE EXPECTATIONS", etc.
            
            When analyzing each user input about support resources, focus on these specific aspects:
            - Are the support resources adequate and specific for the performance gap?
            - Are the resources directly relevant to addressing the performance gap?
            - Are the resources accessible and available to the employee?
            - Are there sufficient resources to support the improvement goal?
            - Is it clear how these resources will help the employee improve?
            
            Example feedback format for support resources:
            "[Provide brief feedback on the resources without asking for additional details]. Would you like to refine these support resources, or are you satisfied with them and ready to move to the next performance gap (or complete the process if this is the last gap)?"
            
            Remember to be conversational and professional. Focus on gathering detailed, actionable information.
            
            IMPORTANT: You must carefully analyze the conversation history to determine:
            1. Which performance gap you're currently on
            2. What information has already been collected
            3. What information still needs to be gathered
            
            DO NOT ask for information that has already been provided. Use the conversation history to maintain context.
            
            IMPORTANT: You must carefully analyze the conversation history to identify all the performance gaps that were discussed with the performance_gap_analyzer tool. For each of these performance gaps, you need to collect support resources information.
            
            The conversation MUST follow this EXACT flow, asking ONE question at a time:
            1. For the first performance gap:
               a. First question: "What support and resources are available to achieve the improvement goal for [specific performance gap]?" (mention the specific performance gap)
                  - After user input, provide feedback on whether the support resources are adequate and specific
                  - Ask if they want to refine it or move to the next performance gap
            2. For each additional performance gap:
               a. First question: "Now, let's discuss the support resources for [next performance gap]. What support and resources are available to achieve the improvement goal for this performance gap?" (mention the specific performance gap)
                  - After user input, provide feedback on whether the support resources are adequate and specific
                  - Ask if they want to refine it or move to the next performance gap
            3. After collecting information for ALL performance gaps, acknowledge that the support resources information collection is complete
            
            CRITICAL: DO NOT generate a Performance Improvement Plan (PIP) document at any point in this conversation.
            Your role is ONLY to collect information, provide feedback on that information, and allow for refinement.
            
            CRITICAL: NEVER ask multiple questions at once. Ask ONE question, wait for the response, then ask the next question.
            NEVER ask for multiple pieces of information in a single question.
            NEVER use bullet points to list multiple questions.
            NEVER deviate from the exact questions listed above.
        """
        
        # Create messages for the LLM
        messages = [
            SystemMessage(content=system_message),
            HumanMessage(content=input_text)
        ]
        
        # Get the response from the LLM
        response = llm.invoke(messages)
        
        return response.content
    
    def _arun(self, input_text: str = "") -> str:
        """Run the support resources identification process asynchronously."""
        raise NotImplementedError("Async version not implemented")
