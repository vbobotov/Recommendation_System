import tkinter as tk
from tkinter import messagebox


class GUI:
    def __init__(self, model, movie_data):
        """
        Инициализация графического интерфейса для рекомендательной системы.
        :param model: Обученная модель SVDModel для генерации рекомендаций.
        :param movie_data: Список с информацией о фильмах.
        """
        self.model = model
        self.movie_data = movie_data
        self.recommendation_count = 10
        self.max_recommendations = 100
        self.user_id = None

        # Создаем главное окно
        self.root = tk.Tk()
        self.root.title("Movie Recommendation System")
        self.root.geometry("600x500")

        # Поле для ввода ID пользователя
        self.label = tk.Label(self.root, text="Введите ваш ID пользователя:")
        self.label.pack(pady=10)
        self.user_id_entry = tk.Entry(self.root)
        self.user_id_entry.pack(pady=5)

        # Кнопка для получения рекомендаций
        self.recommend_button = tk.Button(self.root, text="Получить рекомендации", command=self.show_recommendations)
        self.recommend_button.pack(pady=10)

        # Поле для вывода рекомендаций
        self.recommendations_text = tk.Text(self.root, height=20, width=70)
        self.recommendations_text.pack(pady=10)

        # Кнопка для добавления рекомендаций
        self.more_button = tk.Button(self.root, text="Показать еще", command=self.expand_recommendations)
        self.more_button.pack(pady=5)
        self.more_button.config(state="disabled")

    def show_recommendations(self):
        """
        Отображает первые 10 рекомендаций для введенного ID пользователя.
        """
        try:
            self.user_id = int(self.user_id_entry.get())
            self.recommendation_count = 10  # Сброс к начальному количеству рекомендаций
            recommendations = self.model.recommend_movies(self.user_id, n_recommendations=self.recommendation_count)
            self.display_recommendations(recommendations)

            # Активируем кнопку "Показать еще" только если доступно больше рекомендаций
            if self.recommendation_count < self.max_recommendations:
                self.more_button.config(state="normal")
            else:
                self.more_button.config(state="disabled")
        except IndexError:
            messagebox.showerror("Ошибка", "Введите корректный ID пользователя.")

    def expand_recommendations(self):
        """
        Расширяет список рекомендаций на 10 фильмов, если это возможно.
        """
        self.recommendation_count += 10
        if self.recommendation_count > self.max_recommendations:
            self.recommendation_count = self.max_recommendations
            self.more_button.config(state="disabled")

        recommendations = self.model.recommend_movies(self.user_id, n_recommendations=self.recommendation_count)
        self.display_recommendations(recommendations)

    def display_recommendations(self, recommendations):
        """
        Отображает рекомендации в текстовом поле интерфейса.
        :param recommendations: Список рекомендаций, содержащий ID фильмов и предсказанные рейтинги.
        """
        self.recommendations_text.delete(1.0, tk.END)  # Очищаем текстовое поле
        for movie_id, rating in recommendations:
            movie_info = [movie for movie in self.movie_data if movie[0] == str(movie_id)]
            title = movie_info[0][2] if movie_info else "Unknown Movie"
            self.recommendations_text.insert(tk.END, f"{title} (Прогнозируемый рейтинг: {rating:.2f})\n")

    def run(self):
        """
        Запускает основной цикл интерфейса.
        """
        self.root.mainloop()
