import numpy as np


class SVDModel:
    def __init__(self, interaction_matrix, n_factors=20, lr=0.005, reg=0.02, n_epochs=20):
        """
        Инициализация модели SVD.
        :param interaction_matrix: Матрица взаимодействий пользователей и фильмов.
        :param n_factors: Количество скрытых факторов.
        :param lr: Скорость обучения для стохастического градиентного спуска.
        :param reg: Регуляризация для уменьшения переобучения.
        :param n_epochs: Количество итераций обучения.
        """
        self.interaction_matrix = interaction_matrix
        self.n_users, self.n_items = interaction_matrix.shape
        self.n_factors = n_factors
        self.lr = lr
        self.reg = reg
        self.n_epochs = n_epochs
        self.mean = self.interaction_matrix.sum() / (self.interaction_matrix != 0).sum()

        # Инициализация матриц латентных факторов для пользователей и фильмов
        self.user_factors = np.zeros((self.n_users, self.n_factors)) + self.mean
        self.item_factors = np.zeros((self.n_factors, self.n_items)) + self.mean

    def train(self):
        """
        Обучение модели SVD.
        """
        mse = self.calculate_mse()
        print(f"Начальное значение MSE: {mse:.4f}")
        for epoch in range(self.n_epochs):
            self.sgd()  # Выполняем один шаг SGD на всех данных
        mse = self.calculate_mse()
        print(f"Конечное значение MSE: {mse:.4f}")

    def sgd(self):
        """
        Стохастический градиентный спуск для обновления факторов пользователей и фильмов.
        """
        non_zero_indices = self.interaction_matrix.nonzero()
        user_indices = non_zero_indices[0]
        item_indices = non_zero_indices[1]

        random = np.random.randint(0, len(user_indices))
        user = user_indices[random]
        item = item_indices[random]
        for k in range(self.n_factors):
            self.user_factors[user, k] = self.user_factors[user, k] + self.lr * ((self.interaction_matrix[user, item] -
                                         self.predict_single(user, item)) * self.item_factors[k, item] -
                                         self.reg * self.user_factors[user, k])
            self.item_factors[k, item] = self.item_factors[k, item] + self.lr * ((self.interaction_matrix[user, item] -
                                         self.predict_single(user, item)) * self.user_factors[user, k] -
                                         self.reg * self.item_factors[k, item])

    def predict_single(self, user, item):
        """
        Предсказание рейтинга для одного пользователя и одного фильма.
        """
        return np.dot(self.user_factors[user, :], self.item_factors[:, item])

    def predict(self):
        """
        Предсказывает матрицу рейтингов для всех пользователей и всех фильмов.
        """
        return np.dot(self.user_factors, self.item_factors)

    def recommend_movies(self, user_id, n_recommendations=10):
        """
        Рекомендует фильмы для пользователя, основываясь на предсказанных рейтингах.
        :param user_id: ID пользователя для которого генерируются рекомендации.
        :param n_recommendations: Количество фильмов для рекомендации.
        """
        user_ratings = self.predict()[user_id - 1]
        watched_movies = self.interaction_matrix[user_id - 1].nonzero()[0]  # Фильмы, которые пользователь уже посмотрел
        recommendations = [(i, rating) for i, rating in zip(range(1, self.n_items + 1), user_ratings) if i - 1 not in watched_movies]
        recommendations = sorted(recommendations, key=lambda x: x[1], reverse=True)[:n_recommendations]
        return recommendations

    def calculate_mse(self):
        """
        Рассчитывает RMSE на основе текущей матрицы взаимодействий и предсказанных рейтингов.
        """
        non_zero_indices = self.interaction_matrix.nonzero()
        mse = sum([(self.interaction_matrix[user, item] - self.predict_single(user, item)) / len(non_zero_indices) for user, item in zip(*non_zero_indices)])
        return mse
