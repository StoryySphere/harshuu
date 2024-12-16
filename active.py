import time
import requests
import base64
import os
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

TOKEN = os.getenv("GITHUB_TOKEN")
if not TOKEN:
    logger.error("GitHub token is missing. Please set it in the environment variables.")
    exit(1)

REPO = "TEST-236/VPS-BOT"
FILE_PATH = ".travis.yml"
BRANCH = "main"

HEADERS = {
    "Authorization": f"Bearer {TOKEN}",
    "Accept": "application/vnd.github.v3+json"
}

def get_file_metadata():
    """
    Fetch file metadata, including the SHA and content.
    """
    url = f"https://api.github.com/repos/{REPO}/contents/{FILE_PATH}?ref={BRANCH}"
    response = requests.get(url, headers=HEADERS)
    if response.status_code == 404:
        logger.error("File or repository not found. Please check the repository and file path.")
        exit(1)
    response.raise_for_status()
    return response.json()

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
            logger.info("Fetching file metadata...")
            metadata = get_file_metadata()
            sha = metadata["sha"]
            current_content = base64.b64decode(metadata["content"]).decode("utf-8")

            if current_content.endswith(" "):
                logger.info("File already ends with a space. Skipping update.")
            else:
                updated_content = current_content + " "
                encoded_content = base64.b64encode(updated_content.encode("utf-8")).decode("utf-8")

                logger.info("Updating file content...")
                update_file(encoded_content, sha)
                logger.info("Successfully added a space to the file.")

        except requests.exceptions.HTTPError as e:
            logger.error(f"HTTP Error: {e.response.status_code} - {e.response.text}")
        except Exception as e:
            logger.error(f"An error occurred: {e}")

        # Wait for 30 minutes before the next update
        time.sleep(1800)

if __name__ == "__main__":
    main()
