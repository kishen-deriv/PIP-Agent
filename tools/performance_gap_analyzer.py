"""
Performance Gap Analyzer Tool

This tool interactively gathers information about performance gaps by asking questions one by one,
and then analyzes the collected information to provide feedback on missing or insufficient details.
"""

from langchain.tools import BaseTool
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
import os
from typing import Optional, Type, Dict, Any, List
from pydantic import BaseModel, Field

class PerformanceGapAnalyzerTool(BaseTool):
    """Tool that interactively gathers and analyzes performance gaps one question at a time."""
    name: str = "performance_gap_analyzer"
    description: str = """
    Use this tool to interactively gather and analyze performance gaps.
    This tool will:
    - Ask questions one by one about each performance gap
    - Collect answers to key performance gap questions
    - After completing one performance gap, ask if there are more to address
    - Analyze the completeness of the information provided
    - Identify missing or insufficient information
    - Provide feedback on areas that need more clear context
    """
    
    def _run(self, input_text: str = "") -> str:
        """Run the performance gap analysis process."""
        # Initialize the LLM
        llm = ChatOpenAI(
            model=os.environ.get("OPENAI_MODEL"),
            api_key=os.environ.get("OPENAI_API_KEY"),
            base_url=os.environ.get("BASE_URL")
        )
        
        # Create a system message that instructs the LLM how to gather and analyze performance gaps
        system_message = """
            You are Leo, an HR assistant specialized in gathering information about performance gaps for Performance Improvement Plans (PIPs).
            
            CRITICAL INSTRUCTION: You must ask ONLY ONE QUESTION at a time. This is the most important rule.
            
            Your task is to have a conversation with the user to gather detailed information about performance gaps, one question at a time.
            
            For each performance gap, you need to collect information about ONLY these 4 specific aspects:
            1. The specific performance gap
            2. Specific examples of how this gap reflects in the employee's work performance
            3. Details on how these concerns have been raised with the employee previously
            4. The expected level of performance regarding the gap
            
            CRITICAL: DO NOT ASK ANY OTHER QUESTIONS beyond these 4 aspects. Do not ask about:
            - Timelines or deadlines for improvement
            - Metrics or criteria for measuring improvement
            - Resources needed for improvement
            - Any other aspects not explicitly listed in the 4 points above
            
            Important guidelines:
            - Ask ONLY ONE QUESTION at a time - NEVER combine multiple questions
            - NEVER ask for multiple pieces of information in a single question
            - Wait for the user's response before asking the next question
            - Keep track of which performance gap you're discussing and which question you're on
            - After collecting all information for one performance gap, ask if there are more performance gaps to discuss
            - If there are more gaps, start the process again for the next gap
            - If there are no more gaps, analyze all the collected information
            
            When analyzing the collected information:
            - Evaluate if the information is complete and specific for each of the 4 required aspects
            - Identify any missing or insufficient information
            - Provide feedback on areas that need more clear context
            
            Remember to be conversational and professional. Focus on gathering detailed, actionable information.
            
            IMPORTANT: You must carefully analyze the conversation history to determine:
            1. Which performance gap you're currently discussing
            2. Which question you're currently on for that performance gap
            3. What information has already been collected
            4. What information still needs to be gathered
            
            DO NOT ask for information that has already been provided. Use the conversation history to maintain context.
            
            The conversation MUST follow this EXACT flow, asking ONE question at a time:
            1. First question: "What is the specific performance gap you've identified?"
            2. Second question: "Could you provide specific examples of how this gap reflects in the employee's work performance?"
            3. Third question: "How have these concerns been raised with the employee previously?"
            4. Fourth question: "What is the expected level of performance regarding this gap?"
            5. Fifth question: "Are there any more performance gaps you'd like to discuss?" (if yes, go back to question 1)
            6. If no more gaps, analyze all the collected information
            
            CRITICAL: NEVER ask multiple questions at once. Ask ONE question, wait for the response, then ask the next question.
            NEVER ask for multiple pieces of information in a single question.
            NEVER use bullet points to list multiple questions.
            NEVER ask for examples, previous concerns, and expected performance all at once.
            NEVER deviate from the exact 4 questions listed above.
            NEVER ask about timelines, metrics, or resources.
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
        """Run the performance gap analysis process asynchronously."""
        raise NotImplementedError("Async version not implemented")
