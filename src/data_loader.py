import numpy as np
import pandas as pd


class DataLoader:
    def __init__(self, movie_titles_path, ratings_files):
        """
        Инициализация экземпляра класса.
        :param movie_titles_path: Матрица взаимодействий пользователей и фильмов.
        :param ratings_files: Количество скрытых факторов.
        """
        self.movie_titles_path = movie_titles_path
        self.ratings_files = ratings_files
        self.movies = None
        self.ratings = None
        self.interaction_matrix = None

    def load_movie_titles(self):
        """
        Загружает информацию о фильмах из файла и сохраняет её в виде cписка.
        """
        movies = []

        with open(self.movie_titles_path, 'r', encoding="ISO-8859-1") as file:
            for line in file:
                parts = line.strip().split(",", 2)
                movie_id, year, title = parts[0], parts[1], parts[2]
                movies.append([movie_id, year, title])

        self.movies = movies
        print(f"Загружено {len(self.movies)} фильмов.")

    def load_ratings(self):
        """
        Загружает данные о рейтингах из файлов и сохраняет их в виде DataFrame.
        """
        print("Загрузка оценок из текстовых файлов...")
        all_ratings = []
        current_movie_id = None
        with open(self.ratings_files, 'r') as file:
            for line in file:
                if line.endswith(":\n"):  # идентификатор фильма
                    current_movie_id = int(line[:-2])
                else:
                    user_id, rating, date = line.split(',')
                    all_ratings.append((current_movie_id, int(user_id), int(rating)))
            self.ratings = pd.DataFrame(all_ratings, columns=["MovieID", "UserID", "Rating"])
        print(f"Загружено {len(self.ratings)} оценок.")

    def build_interaction_matrix(self):
        """
        Создает матрицу взаимодействий на основе загруженных данных о фильмах и рейтингах.
        """
        user_ids = self.ratings["UserID"].unique()
        movie_ids = self.ratings["MovieID"].unique()

        user_map = {user_id: i for i, user_id in enumerate(user_ids)}
        movie_map = {movie_id: i for i, movie_id in enumerate(movie_ids)}

        row_indices = self.ratings["UserID"].map(user_map).values
        col_indices = self.ratings["MovieID"].map(movie_map).values
        data = self.ratings["Rating"].values

        self.interaction_matrix = np.zeros((len(user_ids), len(movie_ids)))
        for rating, row, col in zip(data, row_indices, col_indices):
            self.interaction_matrix[row, col] = rating
        print(f"Матрица взаимодействий размером {self.interaction_matrix.shape} создана.")
