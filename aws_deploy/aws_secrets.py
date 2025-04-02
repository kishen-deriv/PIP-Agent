import json
import boto3
from botocore.exceptions import ClientError
import os
from dotenv import load_dotenv

def get_secrets(key):
    """
    Get environment variables from .env file first, falling back to AWS Secrets Manager if no .env file exists
    Args:
        key: The environment variable key to look up
    Returns:
        The value of the environment variable or None if not found
    """
    # Try loading from .env file first
    load_dotenv()
    env_value = os.getenv(key)
    if env_value is not None:
        return env_value

    # Fall back to AWS Secrets Manager
    secret_name = "deriv-ai/pip"
    region_name = "us-east-1"

    # Only create session and fetch secrets if we haven't already
    if not hasattr(get_secrets, '_cached_secrets'):
        session = boto3.session.Session()
        client = session.client(
            service_name='secretsmanager',
            region_name=region_name
        )

        try:
            get_secret_value_response = client.get_secret_value(
                SecretId=secret_name
            )
            get_secrets._cached_secrets = json.loads(get_secret_value_response['SecretString'])
        except ClientError as e:
            print(f"Failed to retrieve secrets: {str(e)}")
            raise e

    return get_secrets._cached_secrets.get(key)