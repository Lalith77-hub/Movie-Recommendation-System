
import os
import requests
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("TMDB_API_KEY")
MOVIE_ID = 1083637

url = f"https://api.themoviedb.org/3/movie/{MOVIE_ID}/keywords"

try:
    response = requests.get(
        url,
        params={"api_key": API_KEY},
        timeout=30
    )

    response.raise_for_status()

    data = response.json()

    print("Kantara keywords:")

    for keyword in data.get("keywords", []):
        print("-", keyword["name"])

except requests.exceptions.RequestException as error:
    print("TMDB connection error:", error)
