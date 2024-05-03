import json
from google.cloud import pubsub_v1, secretmanager
import requests
import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)  # Capture DEBUG, INFO, WARNING, ERROR, CRITICAL

def fetch_gcp_secret(secret_name: str) -> str:
    # Fetch Project ID from Metadata Server
    metadata_server_url = "http://metadata/computeMetadata/v1/project/project-id"
    headers = {"Metadata-Flavor": "Google"}
    project_id = requests.get(metadata_server_url, headers=headers).text
    
    # Create the Secret Manager client.
    client = secretmanager.SecretManagerServiceClient()

    # Build the resource name of the secret.
    secret_version = 'latest'
    name = f"projects/{project_id}/secrets/{secret_name}/versions/{secret_version}"

    # Access the secret version.
    response = client.access_secret_version(request={"name": name})
    secret_string = response.payload.data.decode("UTF-8")
    return secret_string

def publish_to_pubsub(topic_name : str, data : dict) -> bool:
    """Publishes a message to a Google Cloud Pub/Sub topic."""
    # Fetch Project ID from Metadata Server
    metadata_server_url = "http://metadata/computeMetadata/v1/project/project-id"
    headers = {"Metadata-Flavor": "Google"}
    project_id = requests.get(metadata_server_url, headers=headers).text
    # Publish the message to Pub/Sub
    try:
        publisher = pubsub_v1.PublisherClient()
        topic_path = publisher.topic_path(project_id, topic_name)
        data = json.dumps(data).encode("utf-8")
        future = publisher.publish(topic_path, data)
        logger.debug(f"Published message to topic: {topic_name} and project_id: {project_id}")
        return True
    except Exception as e:
        logger.error(f"Failed to publish message: {str(e)}")
        return False