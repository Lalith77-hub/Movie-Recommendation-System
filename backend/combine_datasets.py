
import os
import pandas as pd

print("Loading movie datasets...")

# Read both CSV files
indian_movies = pd.read_csv("data/indian_movies.csv")
worldwide_movies = pd.read_csv("data/worldwide_movies.csv")

# Identify where each movie came from
indian_movies["source"] = "Indian"
worldwide_movies["source"] = "Worldwide"

# Combine both datasets
combined = pd.concat(
    [indian_movies, worldwide_movies],
    ignore_index=True
)

print("Total records before removing duplicates:", len(combined))

# Remove duplicate movies using TMDB movie ID
combined = combined.drop_duplicates(
    subset="movie_id",
    keep="first"
)

# Save the final dataset
os.makedirs("data", exist_ok=True)

combined.to_csv(
    "data/all_movies.csv",
    index=False,
    encoding="utf-8-sig"
)

print("\nDataset combined successfully!")
print("Total unique movies:", len(combined))
print("Indian dataset records:", len(indian_movies))
print("Worldwide dataset records:", len(worldwide_movies))
print("Saved to: data/all_movies.csv")

print("\nSample movies:")
print(
    combined[
        ["title", "language", "release_date", "rating", "source"]
    ].head(10)
)
