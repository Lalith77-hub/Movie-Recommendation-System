
import ast
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

GENRE_MAP = {
    28: "Action", 12: "Adventure", 16: "Animation",
    35: "Comedy", 80: "Crime", 99: "Documentary",
    18: "Drama", 10751: "Family", 14: "Fantasy",
    36: "History", 27: "Horror", 10402: "Music",
    9648: "Mystery", 10749: "Romance",
    878: "Science Fiction", 10770: "TV Movie",
    53: "Thriller", 10752: "War", 37: "Western"
}

print("Loading CineMatch AI movie data...")

movies = pd.read_csv("data/all_movies_with_keywords.csv")

for column in ["overview", "genres", "title", "language", "keywords"]:
    movies[column] = movies[column].fillna("").astype(str)


def convert_genres(genre_data):
    try:
        genre_ids = ast.literal_eval(genre_data)

        if not isinstance(genre_ids, list):
            return ""

        return " ".join(
            GENRE_MAP.get(int(genre_id), "")
            for genre_id in genre_ids
        )

    except (ValueError, SyntaxError, TypeError):
        return ""


movies["genre_names"] = movies["genres"].apply(convert_genres)

# Custom keywords for movies with missing TMDB keywords

custom_keywords = {
    1083637: (
        "Indian folklore mythology mystical forest "
        "kingdom prince royal conflict tradition "
        "fantasy action drama"
    ),

    360814: (
        "Indian sports wrestling athlete women wrestlers "
        "father daughter relationship training competition "
        "determination family biography empowerment"
    )
}
for movie_id, keywords in custom_keywords.items():

    movie_mask = (
        pd.to_numeric(movies["movie_id"], errors="coerce")
        == movie_id
    )

    movies.loc[movie_mask, "keywords"] = keywords

print("Custom movie keywords applied!")


movies["combined_features"] = (
    movies["title"] + " " +
    movies["overview"] + " " +
    movies["genre_names"] + " " +
    movies["language"] + " " +
    movies["keywords"] + " " +
    movies["keywords"]
)

tfidf = TfidfVectorizer(
    stop_words="english",
    max_features=10000
)

tfidf_matrix = tfidf.fit_transform(movies["combined_features"])

similarity_matrix = cosine_similarity(tfidf_matrix)

print("CineMatch AI recommendation model is ready!")



def recommend_movies(movie_name, number_of_recommendations=10):

    search_name = movie_name.strip().lower()

    matches = movies[
        movies["title"].str.strip().str.lower() == search_name
    ]

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
        print("Movie not found. Please try another title.")
        return

    movie_position = movies.index.get_loc(matches.index[0])

    searched_movie = movies.iloc[movie_position]

    print("\nRecommendations based on:", searched_movie["title"])

    similarity_scores = list(
        enumerate(similarity_matrix[movie_position])
    )

    similarity_scores = sorted(
        similarity_scores,
        key=lambda x: x[1],
        reverse=True
    )

    if searched_movie["source"] == "Indian":

        indian_scores = [
            (index, score)
            for index, score in similarity_scores
            if index != movie_position
           and movies.iloc[index]["source"] == "Indian"
and movies.iloc[index]["rating"] > 0
        ]

        recommendations = indian_scores[:number_of_recommendations]

    else:

        recommendations = [
            (index, score)
            for index, score in similarity_scores
            if index != movie_position
        ][:number_of_recommendations]

    print("\nRecommended Movies:")

    for index, score in recommendations:

        movie = movies.iloc[index]

        print(
            f"{movie['title']} | "
            f"Language: {movie['language']} | "
            f"Rating: {movie['rating']} | "
            f"Similarity: {score * 100:.2f}%"
        )


if __name__ == "__main__":
   recommend_movies("Avatar")
