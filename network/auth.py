import os

import requests
from dotenv import load_dotenv

load_dotenv()

AUTH_URL = os.getenv("AUTH_URL")

LOGIN_URL = f"{AUTH_URL}/login"


def login(username: str, password: str):
    if not username or not password:
        return None, "Username and password must be provided."

    print(LOGIN_URL)

    payload = {"username": username, "password": password}

    try:
        response = requests.post(LOGIN_URL, json=payload)

        if response.status_code == 200:
            return response.json(), None
        elif response.status_code == 401:
            return None, "Invalid username or password."
        elif response.status_code == 400:
            return None, "Bad request: missing username or password."
        else:
            return None, "Unknown server error."

    except requests.exceptions.RequestException:
        return None, "Error connecting to the server."
