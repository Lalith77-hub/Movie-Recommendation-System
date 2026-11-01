
import os
import requests
from dotenv import load_dotenv
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

load_dotenv()

API_KEY = os.getenv("TMDB_API_KEY")
BASE_URL = "https://api.themoviedb.org/3"

session = requests.Session()

retry = Retry(
    total=5,
    backoff_factor=2,
    status_forcelist=[429, 500, 502, 503, 504],
    allowed_methods=["GET"]
)

session.mount("https://", HTTPAdapter(max_retries=retry))

movies_to_test = [
    {"title": "Saffron", "id": 786026, "year": 2020},
    {"title": "Sultan", "id": 376812, "year": 2016}
]

for movie in movies_to_test:

    print("\n" + "=" * 50)
    print("MOVIE:", movie["title"])
    print("=" * 50)

    try:
        url = f"{BASE_URL}/movie/{movie['id']}/images"

        response = session.get(
            url,
            params={
                "api_key": API_KEY,
                "include_image_language": "en,null"
            },
            timeout=30
        )

        response.raise_for_status()

        posters = response.json().get("posters", [])

        print("Posters found using ID:", len(posters))

        for poster in posters:
            print("https://image.tmdb.org/t/p/w500" + poster["file_path"])

        search_url = f"{BASE_URL}/search/movie"

        response = session.get(
            search_url,
            params={
                "api_key": API_KEY,
                "query": movie["title"],
                "year": movie["year"]
            },
            timeout=30
        )

        response.raise_for_status()

        print("\nSearch results:")

        for result in response.json().get("results", [])[:5]:
            print(
                result["title"],
                "| ID:", result["id"],
                "| Release:", result.get("release_date"),
                "| Poster:", result.get("poster_path")
            )

    except requests.RequestException as error:
        print("Request failed:", error)

print("\nPoster testing completed!")
