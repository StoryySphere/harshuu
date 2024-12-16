import time
import requests
import base64
import os
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

TOKEN = os.getenv("GITHUB_TOKEN", "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")  # Replace with your token
REPO = "StoryySphere/harshuu"  # Replace with your GitHub username and repository
FILE_PATH = ".travis.yml"  # Ensure this matches the actual file in the repository
BRANCH = "main"  # Ensure this matches the branch name

HEADERS = {
    "Authorization": f"token {TOKEN}",
    "Accept": "application/vnd.github.v3+json"
}

def get_file_sha():
    """
    Get the SHA of the file to modify.
    """
    url = f"https://api.github.com/repos/{REPO}/contents/{FILE_PATH}"
    response = requests.get(url, headers=HEADERS)
    response.raise_for_status()
    return response.json()["sha"]

def get_file_content():
    """
    Fetch the content of the file.
    """
    url = f"https://api.github.com/repos/{REPO}/contents/{FILE_PATH}"
    response = requests.get(url, headers=HEADERS)
    response.raise_for_status()
    return response.json()["content"]

def update_file(new_content, sha):
    """
    Update the file content on GitHub.
    """
    url = f"https://api.github.com/repos/{REPO}/contents/{FILE_PATH}"
    data = {
        "message": "Add space to the end of file",
        "content": new_content,
        "sha": sha,
        "branch": BRANCH
    }
    response = requests.put(url, json=data, headers=HEADERS)
    response.raise_for_status()
    logger.info("File updated successfully.")

def main():
    """
    Main function to periodically update the file.
    """
    while True:
        try:
            logger.info("Fetching file SHA and content...")
            sha = get_file_sha()
            current_content = get_file_content()

            # Decode, modify, and encode the file content
            decoded_content = base64.b64decode(current_content).decode("utf-8")
            updated_content = decoded_content + " "
            encoded_content = base64.b64encode(updated_content.encode("utf-8")).decode("utf-8")

            # Update the file
            logger.info("Updating file content...")
            update_file(encoded_content, sha)
            logger.info("Successfully added a space to the file.")

        except requests.exceptions.HTTPError as e:
            logger.error(f"HTTP Error: {e.response.status_code} - {e.response.text}")
        except Exception as e:
            logger.error(f"An error occurred: {e}")

        # Wait for 30 minutes before the next update
        time.sleep(7200)

if __name__ == "__main__":
    main()
