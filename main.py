from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler
import os
from datetime import datetime
from dotenv import load_dotenv
from src.agent import Leo, langfuse
from prompts.output_format import pip_output_format
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
from aws_deploy.aws_secrets import get_secrets

# Load environment variables
load_dotenv()

# Initialize Slack app - remove signing_secret as it's not needed for Socket Mode
# app = App(token=os.getenv("SLACK_BOT_TOKEN"))
app = App(token=get_secrets("SLACK_BOT_TOKEN"))

# Define the specific private channel ID where the bot should respond
# This should be set in your .env file
# ALLOWED_PRIVATE_CHANNEL_ID = os.getenv("ALLOWED_PRIVATE_CHANNEL_ID")
ALLOWED_PRIVATE_CHANNEL_ID = get_secrets("ALLOWED_PRIVATE_CHANNEL_ID")

# Initialize the Enhanced PIP generator
pip_generator = Leo()

@app.event("app_mention")
def handle_app_mention_events(body, say):
    """Handle when the bot is mentioned"""
    # Check if the mention is from the allowed private channel
    channel_id = body.get("event", {}).get("channel")
    user_id = body.get("event", {}).get("user")
    
    # Create a trace for the app mention event
    trace = langfuse.trace(
        name="app_mention",
        user_id=user_id,
        metadata={
            "channel_id": channel_id
        }
    )
    
    #if channel_id == Config.ALLOWED_PRIVATE_CHANNEL_ID:
    if channel_id == ALLOWED_PRIVATE_CHANNEL_ID:
        say("""Hello! 👋 I'm Leo. Here's what I can do:

                • Use `/generate-pip` command to create a Performance Improvement Plan document
                • I'll guide you through a form where you can input employee details and performance information
                • My enhanced pipeline approach breaks down the PIP generation into specialized steps for better results

                To get started, just type `/generate-pip` in the chat!"""
            )
        trace.event(
                name="response_sent",
                level="DEFAULT",
                message="welcome_message"
            )
    else:
        trace.event(
            name="unauthorized_channel",
            level="WARNING",
            message=f"Unauthorized channel: {channel_id}"
        )

@app.event("message")
def handle_message_events(message, say):
    """Handle direct messages to the bot"""
    # Get the channel ID from the message
    channel_id = message.get('channel')
    user_id = message.get('user')
    message_text = message.get('text', '')
    
    # Create a trace for the message event
    trace = langfuse.trace(
        name="direct_message",
        user_id=user_id,
        metadata={
            "channel_id": channel_id,
            "contains_leo": "Leo" in message_text.lower()
        }
    )
    
    # Only respond if the message is from the allowed private channel
    if channel_id == ALLOWED_PRIVATE_CHANNEL_ID and "Leo" in message_text.lower():
        say("""Hello! 👋 I'm Leo. Here's what I can do:

• Use `/generate-pip` command to create a Performance Improvement Plan document
• I'll guide you through a form where you can input employee details and performance information
• My enhanced pipeline approach breaks down the PIP generation into specialized steps for better results

To get started, just type `/generate-pip` in the chat!""")
        trace.event(
            name="response_sent",
            level="DEFAULT",
            message="welcome_message"
        )
    else:
        trace.event(
            name="no_response_needed",
            level="DEFAULT",
            message="message_ignored"
        )

@app.command("/generate-pip")
def handle_pip_command(ack, body, client):
    """Handle the /generate-pip slash command"""
    # Always acknowledge the command to prevent timeout
    ack()
    
    # Get the channel ID from the command
    channel_id = body.get("channel_id")
    user_id = body.get("user_id")
    
    # Create a trace for the command
    trace = langfuse.trace(
        name="generate_pip_command",
        user_id=user_id,
        metadata={
            "channel_id": channel_id
        }
    )
    
    # Only process if the command is from the allowed private channel
    if channel_id == ALLOWED_PRIVATE_CHANNEL_ID:
        # Open a modal to collect PIP information
        try:
            client.views_open(
                trigger_id=body["trigger_id"],
                view={
            "type": "modal",
            "callback_id": "pip_submission",
            "title": {"type": "plain_text", "text": "Generate PIP"},
            "submit": {"type": "plain_text", "text": "Submit"},
            "blocks": [
                {
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text": "*Leo*\nUses a specialized pipeline approach to create comprehensive PIP documents."
                    }
                },
                {
                    "type": "input",
                    "block_id": "pip_input_block",
                    "element": {
                        "type": "plain_text_input",
                        "multiline": True,
                        "action_id": "pip_input"
                    },
                    "label": {"type": "plain_text", "text": "Enter PIP details"}
                },
                {
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text": "Choose generation method:"
                    }
                },
                {
                    "type": "actions",
                    "block_id": "generation_method",
                    "elements": [
                        {
                            "type": "radio_buttons",
                            "action_id": "pipeline_choice",
                            "options": [
                                {
                                    "text": {
                                        "type": "plain_text",
                                        "text": "Simple (recommended)"
                                    },
                                    "value": "simple"
                                },
                                {
                                    "text": {
                                        "type": "plain_text",
                                        "text": "Pipeline"
                                    },
                                    "value": "pipeline"
                                }
                            ],
                            "initial_option": {
                                "text": {
                                    "type": "plain_text",
                                    "text": "Simple (recommended)"
                                },
                                "value": "simple"
                            }
                        }
                    ]
                }
            ]
                }
            )
            trace.event(
                name="modal_opened",
                level="DEFAULT",
                message="Modal opened successfully"
            )
        except Exception as e:
            error_msg = f"Error opening modal: {str(e)}"
            trace.event(
                name="modal_error",
                level="ERROR",
                message=error_msg
            )
    else:
        trace.event(
            name="unauthorized_channel",
            level="WARNING",
            message=f"Unauthorized channel: {channel_id}"
        )

@app.view("pip_submission")
def handle_pip_submission(ack, body, client, view):
    """Handle the submission of the PIP modal"""
    ack()
    
    user_id = body["user"]["id"]
    
    # Create a trace for the submission
    trace = langfuse.trace(
        name="pip_submission",
        user_id=user_id,
        metadata={
            "submission_type": "pip_form"
        }
    )
    
    try:
        # Get the input from the modal
        pip_input = view["state"]["values"]["pip_input_block"]["pip_input"]["value"]
        
        # Get the generation method choice
        generation_method = view["state"]["values"]["generation_method"]["pipeline_choice"]["selected_option"]["value"]
        use_pipeline = generation_method == "pipeline"
        
        trace.event(
            name="submission_details",
            level="DEFAULT",
            metadata={
                "input_length": len(pip_input),
                "generation_method": generation_method
            }
        )
        
        # Generate the PIP document
        generation_span = trace.span(
            name="generate_pip_document",
            input={
                "input_length": len(pip_input),
                "use_pipeline": use_pipeline
            }
        )
        
        pip_document = pip_generator.generate_pip(
            pip_input_form=pip_input,
            pip_output_format=pip_output_format,
            use_pipeline=use_pipeline
        )
        
        generation_span.end(output={"document_length": len(pip_document)})
        
        # Get the requestor's name from the user info
        user_info = client.users_info(user=user_id)
        requestor_name = user_info["user"]["real_name"]
        
        # Save the document for reference with requestor name in filename
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"pip_document_{timestamp}.txt"
        output_path = f"output/{filename}"
        
        # Add requestor information to the document
        pip_document_with_requestor = f"Generated by: {requestor_name}\n\n{pip_document}"
        
        save_span = trace.span(name="save_document")
        pip_generator.save_pip(pip_document_with_requestor, output_path)
        save_span.end()
        
        # Send as a file attachment
        method_text = "pipeline" if use_pipeline else "simple"
        message = f"Here's your generated PIP document <@{requestor_name}>:"
        
        # Create a WebClient instance using the bot token
        #slack_client = WebClient(token=os.getenv("SLACK_BOT_TOKEN"))
        slack_client = WebClient(token=get_secrets("SLACK_BOT_TOKEN"))

        # First, write the content to a temporary file
        with open(output_path, 'r') as file:
            file_content = file.read()
        
        # Upload the file to Slack using the files_upload_v2 method from slack_sdk
        try:
            upload_span = trace.span(name="upload_file_to_slack")
            result = slack_client.files_upload_v2(
                channel=ALLOWED_PRIVATE_CHANNEL_ID,
                title=f"PIP Document - {timestamp}",
                filename=filename,
                file=output_path,
                initial_comment=message
            )
            upload_span.end()
            
            trace.event(
                name="file_upload",
                level="DEFAULT",
                message="File uploaded successfully",
                metadata={"file_id": result.get("file", {}).get("id")}
            )
            print(f"File uploaded successfully: {result}")
        except SlackApiError as e:
            error_msg = f"Error uploading file: {e}"
            print(error_msg)
            trace.event(
                name="file_upload_error",
                level="ERROR",
                message=error_msg
            )
            # Fallback to chat_postMessage if file upload fails
            slack_client.chat_postMessage(
                channel=ALLOWED_PRIVATE_CHANNEL_ID,
                text=f"Error uploading PIP document {requestor_name}: {str(e)}\n\nHere's the document content:\n\n```\n{pip_document_with_requestor}\n```"
            )
        
    except Exception as e:
        error_msg = f"Error generating PIP document: {str(e)}"
        trace.event(
            name="generation_error",
            level="ERROR",
            message=error_msg
        )
        client.chat_postMessage(
            channel=ALLOWED_PRIVATE_CHANNEL_ID,  # Use the allowed channel ID
            text=error_msg
        )

if __name__ == "__main__":
    # Replace app.start() with SocketModeHandler
    handler = SocketModeHandler(
        app=app,
        #app_token=os.getenv("SLACK_APP_TOKEN")  # You'll need this new token
        app_token=get_secrets("SLACK_APP_TOKEN")
    )
    handler.start()
