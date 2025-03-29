import os
import json
from pathlib import Path
from langgraph.prebuilt import create_react_agent
from langchain_openai import ChatOpenAI
from langchain_anthropic import ChatAnthropic
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
from langgraph.checkpoint.memory import MemorySaver
from dotenv import load_dotenv

import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))

from prompts.agent_system_prompt import agent_system_message

from aws_deploy.aws_secrets import get_secrets
# Import tools
from tools.employee_info_extractor import EmployeeInfoExtractorTool
from tools.performance_gap_analyzer import PerformanceGapAnalyzerTool
from tools.improvement_plan_analyzer import ImprovementPlanAnalyzerTool
from tools.support_resources_identifier import SupportResourcesIdentifierTool
from tools.comprehensive_pip_generator import ComprehensivePIPGeneratorTool

# Load environment variables
load_dotenv()

# Define memory file path for persistence
MEMORY_DIR = Path("./memory")
MEMORY_DIR.mkdir(exist_ok=True)
MEMORY_FILE = MEMORY_DIR / "conversation_memory.json"

def load_conversation_memory(thread_id):
    """Load conversation memory from file if it exists"""
    if MEMORY_FILE.exists():
        try:
            with open(MEMORY_FILE, "r") as f:
                memory_data = json.load(f)
                return memory_data.get(thread_id, {"messages": []})
        except Exception as e:
            print(f"Error loading memory: {e}")
    return {"messages": []}

def save_conversation_memory(thread_id, memory_data):
    """Save conversation memory to file"""
    all_memory = {}
    if MEMORY_FILE.exists():
        try:
            with open(MEMORY_FILE, "r") as f:
                all_memory = json.load(f)
        except Exception as e:
            print(f"Error reading existing memory: {e}")
    
    all_memory[thread_id] = memory_data
    
    try:
        with open(MEMORY_FILE, "w") as f:
            json.dump(all_memory, f, indent=2)
    except Exception as e:
        print(f"Error saving memory: {e}")

def chat_with_memory(user_input, thread_id="default"):
    """Chat with the agent using persistent memory"""
    # Initialize model using ChatOpenAI with LiteLLM proxy
    model = ChatOpenAI(
        model=get_secrets("ANTHROPIC_MODEL"),  # Still use the Anthropic model name
        api_key=get_secrets("API_KEY"),  # Use the Anthropic API key
        base_url=get_secrets("BASE_URL")  # Use the LiteLLM proxy URL
    )
    
    # Initialize memory saver
    memory = MemorySaver()
    
    # Initialize tools
    employee_info_tool = EmployeeInfoExtractorTool()
    performance_gap_tool = PerformanceGapAnalyzerTool()
    improvement_plan_tool = ImprovementPlanAnalyzerTool()
    support_resources_tool = SupportResourcesIdentifierTool()
    comprehensive_pip_tool = ComprehensivePIPGeneratorTool()
    tools = [employee_info_tool, performance_gap_tool, improvement_plan_tool, support_resources_tool, comprehensive_pip_tool]
    
    # Create agent with tools
    agent_executor = create_react_agent(model, checkpointer=memory, tools=tools)
    
    # Load previous conversation if it exists
    conversation = load_conversation_memory(thread_id)
    
    # Add the new user message
    conversation["messages"].append({"role": "human", "content": user_input})
    
    # Convert to LangChain message format
    lc_messages = []
    for msg in conversation["messages"]:
        if msg["role"] == "human":
            lc_messages.append(HumanMessage(content=msg["content"]))
        elif msg["role"] == "ai":
            lc_messages.append(AIMessage(content=msg["content"]))
    
    # Add a system message to help the agent better track conversation history
    if lc_messages:
        # Add a system message to remind the agent to check conversation history and use tools
        system_message = agent_system_message
        lc_messages.insert(0, SystemMessage(content=system_message))
    
    try:
        response = agent_executor.invoke(
            {"messages": lc_messages},
            {"configurable": {"thread_id": thread_id}}
        )

        
        # Extract the AI's response
        ai_message = response["messages"][-1].content
        
        # If AI message is empty, return a default message instead
        if not ai_message:
            ai_message = "I'm processing your request. Could you provide more details?"

    except Exception as e:
        import traceback
        print(f"Error invoking agent: {e}")
        print(f"Detailed error: {traceback.format_exc()}")
        ai_message = "I apologize, but I encountered an error. Please try again."
    
    # Add the AI response to the conversation
    conversation["messages"].append({"role": "ai", "content": ai_message})
    
    # Save the updated conversation
    save_conversation_memory(thread_id, conversation)
    
    return ai_message

# Example usage
if __name__ == "__main__":
    user_input = input("You: ")
    response = chat_with_memory(user_input)
    print(f"AI: {response}")
