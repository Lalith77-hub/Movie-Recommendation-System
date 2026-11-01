
import os
import time
import requests
import pandas as pd
from dotenv import load_dotenv
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

# Load TMDB API key
load_dotenv()
API_KEY = os.getenv("TMDB_API_KEY")

if not API_KEY:
    raise ValueError("TMDB API key not found. Check your .env file.")

BASE_URL = "https://api.themoviedb.org/3/movie/popular"

# Retry temporary connection failures
retry_strategy = Retry(
    total=5,
    connect=5,
    read=5,
    backoff_factor=1,
    status_forcelist=[429, 500, 502, 503, 504],
    allowed_methods=["GET"]
)

session = requests.Session()
adapter = HTTPAdapter(max_retries=retry_strategy)
session.mount("https://", adapter)

movies = []
seen_ids = set()

os.makedirs("data", exist_ok=True)
output_file = "data/worldwide_movies.csv"

print("Collecting worldwide movies from TMDB...")

for page in range(1, 61):
    print(f"Downloading page {page} of 60...")

    params = {
        "api_key": API_KEY,
        "page": page
    }

    try:
        response = session.get(
            BASE_URL,
            params=params,
            timeout=45
        )
        response.raise_for_status()

        results = response.json().get("results", [])

        if not results:
            break

        for movie in results:
            movie_id = movie.get("id")

            if movie_id in seen_ids:
                continue

            seen_ids.add(movie_id)

            movies.append({
                "movie_id": movie_id,
                "title": movie.get("title"),
                "original_title": movie.get("original_title"),
                "language": movie.get("original_language"),
                "release_date": movie.get("release_date"),
                "overview": movie.get("overview"),
                "rating": movie.get("vote_average"),
                "vote_count": movie.get("vote_count"),
                "popularity": movie.get("popularity"),
                "genres": movie.get("genre_ids")
            })

        # Save progress after each page
        pd.DataFrame(movies).to_csv(
            output_file,
            index=False,
            encoding="utf-8-sig"
        )

        print("Movies collected so far:", len(movies))
        time.sleep(0.5)

    except requests.exceptions.RequestException as error:
        print("Connection problem:", error)
        print("Previously collected movies are saved.")
        break

print("\nWorldwide collection completed!")
print("Total movies collected:", len(movies))
print("Saved to:", output_file)

if movies:
    df = pd.DataFrame(movies)
    print("\nSample worldwide movies:")
    print(df[["title", "language", "release_date", "rating"]].head(10))
