from data_loader import DataLoader
from svd_model import SVDModel
from evaluator import Evaluation
from interface import GUI


MOVIE_TITLES_PATH = "../movie_titles0.csv"
RATINGS_FILES = "../combined_data_0.txt"


def main():
    # Шаг 1: Загрузка данных
    print("Загрузка данных...")
    data_loader = DataLoader(MOVIE_TITLES_PATH, RATINGS_FILES)
    data_loader.load_movie_titles()
    data_loader.load_ratings()

    # Шаг 2: Построение матрицы взаимодействий
    print("Построение матрицы взаимодействий...")
    data_loader.build_interaction_matrix()

    # Шаг 3: Обучение модели SVD
    print("Обучение модели SVD...")
    svd_model = SVDModel(interaction_matrix=data_loader.interaction_matrix, n_factors=3, lr=0.01, reg=0.1,
                         n_epochs=50000)
    svd_model.train()

    # Шаг 4: Оценка качества модели
    print("Оценка качества модели...")
    evaluator = Evaluation(svd_model, data_loader.interaction_matrix)
    evaluation_results = evaluator.evaluate()
    print("Результаты оценки:", f"RMSE: {evaluation_results["RMSE"]:.4f}", f"MAE: {evaluation_results["MAE"]:.4f}", sep="\n")

    # Шаг 5: Запуск графического интерфейса для рекомендаций
    print("Запуск интерфейса...")
    gui = GUI(svd_model, data_loader.movies)
    gui.run()


if __name__ == "__main__":
    main()
