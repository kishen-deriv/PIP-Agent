"""
Test script for the interactive Performance Gap Analyzer tool

This script simulates how the agent would use the performance_gap_analyzer tool
with conversation history.
"""

import os
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))

from tools.performance_gap_analyzer import PerformanceGapAnalyzerTool
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def test_interactive_performance_gap_analyzer():
    """Test the interactive performance gap analyzer tool with a simulated conversation history"""
    
    # Initialize the tool and LLM
    performance_gap_tool = PerformanceGapAnalyzerTool()
    llm = ChatOpenAI(
        model=os.environ.get("OPENAI_MODEL"),
        api_key=os.environ.get("OPENAI_API_KEY"),
        base_url=os.environ.get("BASE_URL")
    )
    
    # Simulate a conversation history
    conversation_history = []
    
    # System message for the performance gap analyzer
    system_message = """
        You are Leo, an HR assistant specialized in gathering information about performance gaps for Performance Improvement Plans (PIPs).
        
        Your task is to have a conversation with the user to gather detailed information about performance gaps, one question at a time.
        
        For each performance gap, you need to collect information about:
        1. The specific performance gap
        2. Specific examples of how this gap reflects in the employee's work performance
        3. Details on how these concerns have been raised with the employee previously
        4. The expected level of performance regarding the gap
        
        Important guidelines:
        - Ask only ONE question at a time
        - Wait for the user's response before asking the next question
        - Keep track of which performance gap you're discussing and which question you're on
        - After collecting all information for one performance gap, ask if there are more performance gaps to discuss
        - If there are more gaps, start the process again for the next gap
        - If there are no more gaps, analyze all the collected information
        
        When analyzing the collected information:
        - Evaluate if the information is complete and specific
        - Identify any missing or insufficient information
        - Provide feedback on areas that need more clear context
        
        Remember to be conversational and professional. Focus on gathering detailed, actionable information.
        
        IMPORTANT: You must carefully analyze the conversation history to determine:
        1. Which performance gap you're currently discussing
        2. Which question you're currently on for that performance gap
        3. What information has already been collected
        4. What information still needs to be gathered
        
        DO NOT ask for information that has already been provided. Use the conversation history to maintain context.
        
        The conversation should follow this general flow:
        1. Ask for the specific performance gap
        2. Ask for specific examples of how this gap reflects in the employee's work performance
        3. Ask for details on how these concerns have been raised with the employee previously
        4. Ask for the expected level of performance regarding the gap
        5. Ask if there are more performance gaps to discuss
        6. If yes, go back to step 1 for the next gap
        7. If no, analyze all the collected information
        
        NEVER ask multiple questions at once. Ask ONE question, wait for the response, then ask the next question.
    """
    
    print("\n=== Starting Performance Gap Analysis ===\n")
    
    # Start the conversation
    user_input = "I need to analyze a performance gap for an employee."
    print(f"User: {user_input}\n")
    
    # Add to conversation history
    conversation_history.append(HumanMessage(content=user_input))
    
    # Get the first question from the tool
    messages = [SystemMessage(content=system_message)] + conversation_history
    response = llm.invoke(messages)
    print(f"Tool: {response.content}\n")
    
    # Add to conversation history
    conversation_history.append(AIMessage(content=response.content))
    
    # Simulate user responses for the first performance gap
    user_responses = [
        "Lack of Progress and Proactive Action on the Visual Automation Tool Evaluation",
        "Throughout Q4, there were no regular progress updates provided until specifically requested. This lack of initiative in communicating progress made it difficult to assess the status of the project and delayed decision-making.",
        "On November 12, 2024, during our catch-up call, I raised concerns about the lack of progress on the visual automation tool evaluation. I instructed the employee to create a clear comparison sheet documenting the tools tested, including a list of must-have features. I provided an example of a comparison sheet for reference. During the call, I also emphasized the need for consistent progress updates and instructed them to provide status updates every Thursday or, at the latest, by Friday.",
        "The expected performance is to evaluate and finalize the visual automation tool by the end of Q4. During the evaluation, they are expected to proactively communicate with vendors and team members to ensure milestones are met. As a team lead, they must address technical challenges and provide regular, concise, and accurate progress updates. By the end of Q4, they should have completed the evaluation and selected a visual automation tool based on the outcome."
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
    
    # Indicate no more performance gaps
    user_input = "No, that's all the performance gaps I want to discuss."
    print(f"User: {user_input}\n")
    
    # Add to conversation history
    conversation_history.append(HumanMessage(content=user_input))
    
    # Get the final analysis from the tool
    messages = [SystemMessage(content=system_message)] + conversation_history
    final_response = llm.invoke(messages)
    print(f"Tool: {final_response.content}\n")
    
    print("\n=== Performance Gap Analysis Complete ===\n")
    
    return final_response.content

if __name__ == "__main__":
    test_interactive_performance_gap_analyzer()
