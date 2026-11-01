
import os
import time
import pandas as pd
import requests

from dotenv import load_dotenv
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

load_dotenv()

API_KEY = os.getenv("TMDB_API_KEY")

INPUT_FILE = "data/all_movies.csv"
OUTPUT_FILE = "data/all_movies_with_keywords.csv"

if not API_KEY:
    raise ValueError("TMDB API key not found. Check your .env file.")

print("Loading movie dataset...")

movies = pd.read_csv(INPUT_FILE)

if "keywords" not in movies.columns:
    movies["keywords"] = ""

# Retry settings for connection problems
retry_strategy = Retry(
    total=5,
    connect=5,
    read=5,
    backoff_factor=2,
    status_forcelist=[429, 500, 502, 503, 504],
    allowed_methods=["GET"]
)

session = requests.Session()
adapter = HTTPAdapter(max_retries=retry_strategy)
session.mount("https://", adapter)

print("Total movies:", len(movies))
print("Starting keyword collection...\n")

for index, movie in movies.iterrows():

    # Skip movies whose keywords are already collected
    if pd.notna(movie["keywords"]) and str(movie["keywords"]).strip():
        continue

    movie_id = movie["movie_id"]

    url = f"https://api.themoviedb.org/3/movie/{int(movie_id)}/keywords"

    try:
        response = session.get(
            url,
            params={"api_key": API_KEY},
            timeout=30
        )

        response.raise_for_status()

        data = response.json()

        keyword_list = data.get("keywords", [])

        keywords = " ".join(
            keyword["name"] for keyword in keyword_list
        )

        movies.at[index, "keywords"] = keywords

        print(
            f"{index + 1}/{len(movies)} - "
            f"{movie['title']}: {keywords if keywords else 'No keywords'}"
        )

    except (requests.exceptions.RequestException, ValueError) as error:

        print(f"Error for {movie['title']}: {error}")

    # Save progress after every 25 movies
    if (index + 1) % 25 == 0:
        movies.to_csv(OUTPUT_FILE, index=False, encoding="utf-8-sig")
        print("Progress saved.")

    time.sleep(0.3)

# Final save
movies.to_csv(OUTPUT_FILE, index=False, encoding="utf-8-sig")

print("\nKeyword collection completed!")
print("Saved file:", OUTPUT_FILE)
print("Total movies:", len(movies))
print(
    "Movies with keywords:",
    (movies["keywords"].fillna("").str.strip() != "").sum()
)
