import os
import requests
from dotenv import load_dotenv

# Load API key from .env
load_dotenv()

API_KEY = os.getenv("TMDB_API_KEY")

if not API_KEY:
    print("API key not found. Check your .env file.")
else:
    url = "https://api.themoviedb.org/3/movie/popular"

    response = requests.get(
        url,
        params={"api_key": API_KEY},
        timeout=20
    )

    print("Status Code:", response.status_code)

    if response.status_code == 200:
        print("TMDB connected successfully!")
        movies = response.json()["results"]

        for movie in movies[:5]:
            print(movie["title"])
    else:
        print("Connection failed. Check your API key.")