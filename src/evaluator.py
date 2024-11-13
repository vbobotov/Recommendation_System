class Evaluation:
    def __init__(self, model, interaction_matrix):
        """
        Инициализация класса оценки модели.
        :param model: Обученная модель SVDModel, которая будет использоваться для предсказания.
        :param interaction_matrix: Матрица взаимодействий пользователей и фильмов.
        """
        self.model = model
        self.interaction_matrix = interaction_matrix
        self.n_users, self.n_items = self.interaction_matrix.shape
        self.predict = model.predict()

    def calculate_rmse(self):
        """
        Вычисляет среднеквадратичную ошибку (RMSE) для модели на основе существующих данных взаимодействий.
        """
        non_zero_indices = self.interaction_matrix.nonzero()
        rmse = (sum([(self.interaction_matrix[user, item] - self.predict[user, item]) / non_zero_indices[0].shape[0] for
                   user, item in zip(*non_zero_indices)])) ** 0.5
        return rmse

    def calculate_mae(self):
        """
        Вычисляет среднюю абсолютную ошибку (MAE) для модели на основе существующих данных взаимодействий.
        """
        non_zero_indices = self.interaction_matrix.nonzero()
        mae = sum([abs(self.interaction_matrix[user, item] - self.predict[user, item]) / non_zero_indices[0].shape[0] for
                   user, item in zip(*non_zero_indices)])
        return mae

    def evaluate(self):
        """
        Выполняет полную оценку модели, вычисляя RMSE и MAE.
        """
        rmse = self.calculate_rmse()
        mae = self.calculate_mae()
        return {"RMSE": rmse, "MAE": mae}
