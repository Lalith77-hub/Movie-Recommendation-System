
import os
import requests
import pandas as pd

from functools import lru_cache
from dotenv import load_dotenv
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
from flask import Flask, render_template, request
from backend.recommender import movies, similarity_matrix

load_dotenv()

API_KEY = os.getenv("TMDB_API_KEY")
IMAGE_BASE_URL = "https://image.tmdb.org/t/p/w500"
BASE_URL = "https://api.themoviedb.org/3"

# Create a session with automatic retries
session = requests.Session()

retry = Retry(
    total=3,
    connect=3,
    read=3,
    backoff_factor=1,
    status_forcelist=[429, 500, 502, 503, 504],
    allowed_methods=["GET"]
)

session.mount("https://", HTTPAdapter(max_retries=retry))

app = Flask(
    __name__,
    template_folder="frontend/templates",
    static_folder="frontend/static"
)


@lru_cache(maxsize=3000)
def get_movie_poster(movie_id, movie_title, release_date=""):

    if not API_KEY:
        return None

    try:

        # Step 1: Check the movie details using its TMDB ID
        if movie_id:

            details_url = f"{BASE_URL}/movie/{int(movie_id)}"

            response = session.get(
                details_url,
                params={"api_key": API_KEY},
                timeout=20
            )

            if response.status_code == 200:

                poster_path = response.json().get("poster_path")

                if poster_path:
                    return IMAGE_BASE_URL + poster_path

        # Step 2: Check all available posters using the movie ID
        if movie_id:

            images_url = f"{BASE_URL}/movie/{int(movie_id)}/images"

            response = session.get(
                images_url,
                params={
                    "api_key": API_KEY,
                    "include_image_language": "en,null"
                },
                timeout=20
            )

            if response.status_code == 200:

                posters = response.json().get("posters", [])

                if posters:

                    poster_path = posters[0].get("file_path")

                    if poster_path:
                        return IMAGE_BASE_URL + poster_path

        # Step 3: Search using movie title and release year
        search_url = f"{BASE_URL}/search/movie"

        search_params = {
            "api_key": API_KEY,
            "query": movie_title
        }

        if release_date and pd.notna(release_date):

            year = str(release_date)[:4]

            if year.isdigit():
                search_params["year"] = year

        response = session.get(
            search_url,
            params=search_params,
            timeout=20
        )

        if response.status_code == 200:

            results = response.json().get("results", [])

            target_title = str(movie_title).strip().lower()
            target_year = str(release_date)[:4] if release_date else ""

            # Prefer exact title and matching year
            for result in results:

                result_title = result.get("title", "").strip().lower()
                result_year = result.get("release_date", "")[:4]
                poster_path = result.get("poster_path")

                if (
                    result_title == target_title
                    and poster_path
                    and (not target_year or result_year == target_year)
                ):

                    return IMAGE_BASE_URL + poster_path

            # Use exact title if a matching-year result is unavailable
            for result in results:

                result_title = result.get("title", "").strip().lower()
                poster_path = result.get("poster_path")

                if result_title == target_title and poster_path:
                    return IMAGE_BASE_URL + poster_path

    except (requests.RequestException, ValueError, TypeError) as error:

        print(f"Poster error for {movie_title}: {error}")

    return None


@app.route("/", methods=["GET", "POST"])
def home():

    recommendations = []
    searched_movie = ""
    error = None
    movie_name = ""

    if request.method == "POST":

        movie_name = request.form.get("movie_name", "").strip()

        if movie_name:

            # First search for an exact movie title
            matches = movies[
                movies["title"].str.strip().str.lower()
                == movie_name.lower()
            ]

            # If exact match is unavailable, search partially
            if matches.empty:

                matches = movies[
                    movies["title"].str.contains(
                        movie_name,
                        case=False,
                        na=False,
                        regex=False
                    )
                ]

            if matches.empty:

                error = "Movie not found. Please try another title."

            else:

                movie_position = movies.index.get_loc(matches.index[0])

                searched = movies.iloc[movie_position]
                searched_movie = searched["title"]

                scores = list(
                    enumerate(similarity_matrix[movie_position])
                )

                scores = sorted(
                    scores,
                    key=lambda x: x[1],
                    reverse=True
                )

                # Remove the searched movie and unrated movies
                valid_scores = []

                for index, score in scores:

                    if index == movie_position:
                        continue

                    movie = movies.iloc[index]

                    rating = pd.to_numeric(
                        movie["rating"],
                        errors="coerce"
                    )

                    if pd.isna(rating) or rating <= 0:
                        continue

                    # Indian movies get Indian recommendations
                    if searched["source"] == "Indian":

                        if movie["source"] != "Indian":
                            continue

                    valid_scores.append((index, score))

                # Display the top 12 recommendations
                for index, score in valid_scores[:12]:

                    movie = movies.iloc[index]

                    poster = get_movie_poster(
                        int(movie["movie_id"]),
                        str(movie["title"]),
                        str(movie.get("release_date", ""))
                    )

                    recommendations.append({
                        "title": movie["title"],
                        "rating": movie["rating"],
                        "language": movie["language"],
                        "similarity": round(score * 100, 2),
                        "poster": poster
                    })

        else:

            error = "Please enter a movie name."

    return render_template(
        "index.html",
        recommendations=recommendations,
        searched_movie=searched_movie,
        movie_name=movie_name,
        error=error
    )


@app.route("/analytics")
def analytics():
    return render_template("analytics.html")


@app.route("/about")
def about():
    return render_template("about.html")


if __name__ == "__main__":

    print("Starting CineMatch AI...")

    app.run(debug=True)
