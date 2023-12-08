import json,os
import pytest 
from dotenv import load_dotenv


def test_getenv():


    current_directory = os.getcwd()
    parent_directory = os.path.dirname(current_directory)

    # Construct the path to the .env file in the parent directory
    dotenv_path = os.path.join(parent_directory, '.env')

    # Load the environment variables from the .env file
    load_dotenv(dotenv_path)

    with open(os.getenv('API_KEY_PATH')) as f:
        d = json.load(f)
        api_key = d.get("api_key")
        api_secret = d.get("secret_key")
    
    assert d is not None
    assert (api_key is not None)
    assert (api_secret is not None)
