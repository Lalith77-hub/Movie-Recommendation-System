
import os
import pandas as pd
import matplotlib.pyplot as plt

# Load movie dataset
movies = pd.read_csv("data/all_movies_with_keywords.csv")

# Convert columns into numbers
movies["rating"] = pd.to_numeric(
    movies["rating"], errors="coerce"
)

movies["vote_count"] = pd.to_numeric(
    movies["vote_count"], errors="coerce"
)

# Keep movies with at least 50 votes
movies = movies[
    (movies["vote_count"] >= 50) &
    (movies["rating"].notna())
]

# Select top 10 highest-rated movies
top_movies = movies.nlargest(10, "rating").sort_values("rating")

# Create graphs folder
os.makedirs("graphs", exist_ok=True)

# Draw horizontal bar chart
plt.figure(figsize=(12, 7))

bars = plt.barh(
    top_movies["title"],
    top_movies["rating"]
)

# Add rating values
for bar, rating in zip(bars, top_movies["rating"]):
    plt.text(
        rating + 0.03,
        bar.get_y() + bar.get_height() / 2,
        f"{rating:.2f}",
        va="center"
    )

plt.title("Top 10 Highest-Rated Movies (Minimum 50 Votes)")
plt.xlabel("Movie Rating")
plt.ylabel("Movie Title")
plt.xlim(0, 10)

plt.tight_layout()

# Save graph
plt.savefig(
    "graphs/top_10_highest_rated_movies.png",
    dpi=300
)

plt.show()

# GRAPH 2: Movies Released Per Year

# Convert release date into datetime
movies["release_date"] = pd.to_datetime(
    movies["release_date"],
    errors="coerce"
)

# Extract release year
movies["year"] = movies["release_date"].dt.year

# Count movies released each year
yearly_movies = movies["year"].value_counts().sort_index()

# Create line graph
plt.figure(figsize=(12, 6))

plt.plot(
    yearly_movies.index,
    yearly_movies.values,
    marker="o"
)

plt.title("Number of Movies Released Per Year")
plt.xlabel("Release Year")
plt.ylabel("Number of Movies")
plt.grid(True, alpha=0.3)

plt.tight_layout()

# Save graph
plt.savefig(
    "graphs/movies_released_per_year.png",
    dpi=300
)

plt.show()

print("\nYear-wise movie graph created successfully!")
print(yearly_movies.tail(10))


# GRAPH 3: Movie Genre Distribution

import ast
from collections import Counter

genre_map = {
    28: "Action",
    12: "Adventure",
    16: "Animation",
    35: "Comedy",
    80: "Crime",
    99: "Documentary",
    18: "Drama",
    10751: "Family",
    14: "Fantasy",
    36: "History",
    27: "Horror",
    10402: "Music",
    9648: "Mystery",
    10749: "Romance",
    878: "Science Fiction",
    10770: "TV Movie",
    53: "Thriller",
    10752: "War",
    37: "Western"
}

genre_counts = Counter()

for genre_list in movies["genres"].dropna():

    try:
        genre_ids = ast.literal_eval(genre_list)

        for genre_id in genre_ids:
            genre_id = int(genre_id)

            if genre_id in genre_map:
                genre_counts[genre_map[genre_id]] += 1

    except (ValueError, TypeError, SyntaxError):
        continue

top_genres = genre_counts.most_common()

genre_names = [item[0] for item in top_genres]
genre_values = [item[1] for item in top_genres]

plt.figure(figsize=(12, 7))

plt.barh(genre_names[::-1], genre_values[::-1])

plt.title("Movie Genre Distribution")
plt.xlabel("Number of Movies")
plt.ylabel("Movie Genre")

plt.tight_layout()

plt.savefig(
    "graphs/genre_distribution.png",
    dpi=300
)


# GRAPH 4: Language-wise Movie Distribution

# Count movies in each language
language_counts = movies["language"].dropna().value_counts()

# Select top 15 languages
top_languages = language_counts.head(15).sort_values()

# Create bar chart
plt.figure(figsize=(12, 7))

plt.barh(
    top_languages.index,
    top_languages.values
)

plt.title("Movie Distribution by Language")
plt.xlabel("Number of Movies")
plt.ylabel("Language")

plt.tight_layout()

# Save graph
plt.savefig(
    "graphs/language_distribution.png",
    dpi=300
)

plt.show()

print("\nLanguage distribution graph created successfully!")
print(language_counts.head(15).to_string())


# GRAPH 5: Movie Rating Distribution

# Remove invalid ratings
rating_data = movies["rating"].dropna()

# Create histogram
plt.figure(figsize=(12, 6))

plt.hist(
    rating_data,
    bins=10,
    edgecolor="black"
)

plt.title("Movie Rating Distribution")
plt.xlabel("Movie Rating")
plt.ylabel("Number of Movies")

plt.xticks(range(0, 11))
plt.grid(axis="y", alpha=0.3)

plt.tight_layout()

# Save graph
plt.savefig(
    "graphs/rating_distribution.png",
    dpi=300
)

plt.show()

print("\nRating distribution graph created successfully!")
print(rating_data.describe())



plt.show()

print("\nGenre distribution graph created successfully!")
print(top_genres)


print("Graph created successfully!")
print(
    top_movies[
        ["title", "rating", "vote_count"]
    ].sort_values("rating", ascending=False).to_string(index=False)
)
