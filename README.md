# 🎬 Movie Recommendation System

A smart movie recommendation web application built using Python and Machine Learning. It recommends movies based on their content, genres, descriptions, languages and keywords.

## 📌 Project Overview

The Movie Recommendation System helps users discover movies similar to the movie they search for. It uses Content-Based Filtering to analyse movie information and recommend relevant titles.

The project includes Indian and worldwide movies, movie posters (when available), and visual analytics.

## ✨ Features

- Search for movies by title.
- Get recommendations based on movie content.
- Supports Indian and worldwide movies.
- Displays movie posters when available.
- Shows movie ratings and related information.
- Provides an Analytics page with visual graphs.
- Includes a project About page.
- Handles empty and invalid movie searches.

## 🛠️ Technologies Used

| Technology | Purpose |
|---|---|
| Python | Main programming language |
| Flask | Web application framework |
| Pandas | Data processing |
| NumPy | Numerical operations |
| Scikit-learn | Machine Learning |
| TF-IDF | Text feature extraction |
| Cosine Similarity | Movie similarity calculation |
| HTML and CSS | Frontend development |
| TMDB API | Movie information and posters |
| Matplotlib and Seaborn | Data visualization |

## 🤖 Algorithm Used

**Content-Based Filtering**

The system uses two main techniques:

1. **TF-IDF (Term Frequency-Inverse Document Frequency):** Converts movie text information into numerical vectors.
2. **Cosine Similarity:** Measures how similar two movie vectors are and helps identify movies with similar content.

The system considers movie titles, descriptions, genres, languages and keywords to generate recommendations.

## 📊 Data Visualization

The project includes the following graphs:

- Top 10 highest-rated movies.
- Movies released per year.
- Genre distribution.
- Language distribution.
- Rating distribution.

## 📁 Project Structure

```text
Movie-Recommendation-System/
│
├── app.py
├── .gitignore
│
├── backend/
│   ├── collect_indian_movies.py
│   ├── collect_worldwide_movies.py
│   ├── collect_movie_keywords.py
│   ├── combine_datasets.py
│   ├── create_visualizations.py
│   └── recommender.py
│
├── data/
│   ├── all_movies.csv
│   ├── all_movies_with_keywords.csv
│   ├── indian_movies.csv
│   └── worldwide_movies.csv
│
├── frontend/
│   ├── templates/
│   └── static/
│
└── graphs/
```

## ⚙️ Installation and Execution

### 1. Clone the repository

```bash
git clone https://github.com/Lalith77-hub/Movie-Recommendation-System.git
```

### 2. Open the project folder

```bash
cd Movie-Recommendation-System
```

### 3. Create a virtual environment

```bash
python -m venv .venv
```

### 4. Activate the virtual environment (Windows PowerShell)

```powershell
.venv\Scripts\Activate.ps1
```

### 5. Install required libraries

```bash
pip install pandas numpy scikit-learn flask matplotlib seaborn joblib requests python-dotenv
```

### 6. Configure TMDB API

Create a `.env` file in the main project folder and add your own TMDB API key:

```text
TMDB_API_KEY=your_api_key_here
```

Never upload your private API key to GitHub.

### 7. Run the application

```bash
python app.py
```

Open your browser and visit:

```text
http://127.0.0.1:5000
```

## 🔮 Future Enhancements

- Add user login and profiles.
- Improve recommendations with more movie data.
- Add user ratings and feedback.
- Deploy the application online.
- Improve recommendation accuracy.

## 👨‍💻 Author

**Lalith G**

BCA Project – Movie Recommendation System

---

⭐ If you find this project interesting, feel free to explore the repository!