import os
import requests
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("CRICKET_API_KEY")

def get_matches():

    url = f"https://api.cricapi.com/v1/currentMatches?apikey={API_KEY}&offset=0"

    res = requests.get(url)

    data = res.json()

    return data["data"]