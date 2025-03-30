from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler
import os
import time
from datetime import datetime
from dotenv import load_dotenv
from src.agent import chat_with_memory
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
from aws_deploy.aws_secrets import get_secrets
from langfuse import Langfuse

# Set to track recently processed messages to avoid duplicates
processed_messages = set()

# Load environment variables
#load_dotenv()

# Initialize Slack app - remove signing_secret as it's not needed for Socket Mode
# app = App(token=os.getenv("SLACK_BOT_TOKEN"))
slack_token = get_secrets("SLACK_BOT_TOKEN")
app = App(token=slack_token)
client = WebClient(token=slack_token)

# Initialize Langfuse
langfuse = Langfuse(
    secret_key=get_secrets("LANGFUSE_SECRET_KEY"),
    public_key=get_secrets("LANGFUSE_PUBLIC_KEY"),
    host=get_secrets("LANGFUSE_HOST")
)

@app.event("app_mention")
def handle_app_mention_events(body, say):
    """Handle when the bot is mentioned"""
    # Get channel and user info
    event = body.get("event", {})
    channel_id = event.get("channel")
    user_id = event.get("user")
    message_text = event.get("text", "")
    message_ts = event.get("ts")
    
    # Create a unique identifier for this message
    message_id = f"{channel_id}:{message_ts}"
    
    # Skip if we've already processed this message
    if message_id in processed_messages:
        print(f"Skipping already processed message: {message_id}")
        return
    
    # Add to processed messages
    processed_messages.add(message_id)
    
    # Get thread_ts if the message is part of a thread
    thread_ts = event.get("thread_ts")
    
    # Create a trace for the app mention event
    trace = langfuse.trace(
        name="app_mention",
        user_id=user_id,
        metadata={
            "channel_id": channel_id,
            "in_thread": thread_ts is not None
        }
    )
    
    # Log the mention event for debugging
    print(f"Mention received from user {user_id} in channel {channel_id}")
    print(f"Message text: {message_text}")
    
    # Only respond to DMs (im) or App Home
    channel_type = event.get("channel_type")
    if channel_type == "im" or channel_type == "app_home":
        # Add eyes emoji reaction to show we're processing
        message_ts = event.get("ts")
        try:
            client.reactions_add(
                channel=channel_id,
                name="eyes",
                timestamp=message_ts
            )
        except SlackApiError as e:
            print(f"Error adding reaction: {e}")
        # Always respond in a thread
        # If message is already in a thread, use that thread_ts
        # If not, create a new thread using the message's ts
        thread_ts_to_use = thread_ts if thread_ts else event.get("ts")
        
        # Generate a response using the agent
        # Use thread_ts_to_use to ensure each thread has its own conversation memory
        thread_id = f"slack-{channel_id}-{thread_ts_to_use}"
        response = chat_with_memory(message_text, thread_id=thread_id)
        
        # Remove eyes emoji reaction before sending response
        try:
            client.reactions_remove(
                channel=channel_id,
                name="eyes",
                timestamp=message_ts
            )
        except SlackApiError as e:
            print(f"Error removing reaction: {e}")
            
        say(text=response, channel=channel_id, thread_ts=thread_ts_to_use)
        
        print(f"Response sent to channel {channel_id}")
        
        trace.event(
            name="response_sent",
            level="DEFAULT",
            message="agent_response"
        )
    else:
        # Log that we're not responding to this channel type
        print(f"Not responding to mention in channel type: {channel_type}")
        trace.event(
            name="no_response_channel_type",
            level="DEFAULT",
            message=f"Not responding to channel type: {channel_type}"
        )

@app.event("message")
def handle_message_events(body, say):
    """Handle direct messages to the bot"""
    # Get the message details
    event = body.get("event", {})
    channel_id = event.get("channel")
    user_id = event.get("user")
    message_text = event.get("text", "")
    message_ts = event.get("ts")
    
    # Create a unique identifier for this message
    message_id = f"{channel_id}:{message_ts}"
    
    # Skip if we've already processed this message
    if message_id in processed_messages:
        print(f"Skipping already processed message: {message_id}")
        return
    
    # Add to processed messages
    processed_messages.add(message_id)
    
    # Get thread_ts if the message is part of a thread
    thread_ts = event.get("thread_ts")
    
    # Log the message for debugging
    print(f"Message received: '{message_text}' from user {user_id} in channel {channel_id}")
    
    # Create a trace for the message event
    trace = langfuse.trace(
        name="direct_message",
        user_id=user_id,
        metadata={
            "channel_id": channel_id,
            "message_text": message_text,
            "in_thread": thread_ts is not None
        }
    )
    
    # Only respond to DMs (im) or App Home
    channel_type = event.get("channel_type")
    if channel_type == "im" or channel_type == "app_home":
        # Skip messages from bots to prevent loops
        if event.get("bot_id"):
            return
            
        # Add eyes emoji reaction to show we're processing
        message_ts = event.get("ts")
        try:
            client.reactions_add(
                channel=channel_id,
                name="eyes",
                timestamp=message_ts
            )
        except SlackApiError as e:
            print(f"Error adding reaction: {e}")
            
        # Always respond in a thread
        # If message is already in a thread, use that thread_ts
        # If not, create a new thread using the message's ts
        thread_ts_to_use = thread_ts if thread_ts else event.get("ts")
        
        # Generate a response using the agent
        # Use thread_ts_to_use to ensure each thread has its own conversation memory
        thread_id = f"slack-{channel_id}-{thread_ts_to_use}"
        response = chat_with_memory(message_text, thread_id=thread_id)
        
        # Remove eyes emoji reaction before sending response
        try:
            client.reactions_remove(
                channel=channel_id,
                name="eyes",
                timestamp=message_ts
            )
        except SlackApiError as e:
            print(f"Error removing reaction: {e}")
            
        say(text=response, channel=channel_id, thread_ts=thread_ts_to_use)
        
        print(f"Response sent to channel {channel_id}")
        
        trace.event(
            name="response_sent",
            level="DEFAULT",
            message="agent_response"
        )
    else:
        # Log that we're not responding to this channel type
        print(f"Not responding to message in channel type: {channel_type}")
        trace.event(
            name="no_response_channel_type",
            level="DEFAULT",
            message=f"Not responding to channel type: {channel_type}"
        )


if __name__ == "__main__":
    # Print startup message
    print("Starting Leo PIP Agent bot...")
    print("Bot will only respond to DMs and App Home, not in channels")
    
    # Limit the size of the processed_messages set to avoid memory issues
    # This will be enough to prevent duplicates within a reasonable time window
    MAX_PROCESSED_MESSAGES = 1000
    
    # Replace app.start() with SocketModeHandler
    handler = SocketModeHandler(
        app=app,
        #app_token=os.getenv("SLACK_APP_TOKEN")  # You'll need this new token
        app_token=get_secrets("SLACK_APP_TOKEN")
    )
    handler.start()
