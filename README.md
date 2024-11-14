# Система рекомендаций фильмов

## Оглавление
- [Описание проекта](#описание-проекта)
- [Архитектура проекта](#архитектура-проекта)
- [Шаги разработки](#шаги-разработки)

## Описание проекта
Этот проект на Python предназначен для создания простой системы рекомендаций фильмов с использованием коллаборативной фильтрации. Цель проекта — предсказать, какие фильмы могут понравиться пользователю, основываясь на его предыдущих оценках и оценках других пользователей. Система использует датасет, содержащий оценки пользователей, и алгоритм SVD (сингулярное разложение) для генерации рекомендаций.

## Архитектура проекта
Проект структурирован на несколько модульных компонентов, каждый из которых представлен отдельным классом для улучшения читаемости и поддержки кода. Ниже описаны основные классы и их обязанности:

### Классы
1. **`DataLoader`**
    - **Описание**: Отвечает за загрузку и обработку данных об оценках и информации о фильмах из файлов.
    - **Атрибуты**: 
        - `ratings_files`: Путь к TXT файлам с оценками пользователей.
        - `movie_titles_path`: Путь к CSV файлу с информацией о фильмах.
        - `movies`: Список с информацией о фильмах.
        - `ratings`: DataFrame с оценками пользователей.
        - `interaction_matrix`: Матрица взаимодействий пользователей и фильмов.
    - **Магические методы**:
        - `__init__(self, movie_titles_path, ratings_files)`: Инициализирует пути к файлам.
    - **Методы**:
        - `load_ratings(self)`: Загружает данные об оценках пользователей из файла и преобразует их в формат DataFrame.
        - `load_movie_titles(self)`: Загружает данные о фильмах, такие как названия, ID и год выпуска.
        - `build_interaction_matrix(self)`: Создаёт матрицу взаимодействий.

2. **`SVDModel`**
    - **Описание**: Реализует алгоритм SVD для предсказания оценок фильмов и генерации рекомендаций.
    - **Атрибуты**:
        - `n_factors`: Количество скрытых факторов для разложения SVD.
        - `lr`: Шаг стохастического градиентного спуска.
        - `reg`: Скорость регуляризации.
        - `n_epochs`: Колчиество итераций обучения.
        - `interaction_matrix`: Матрица взаимодействий пользователей и фильмов.
        - `n_users`: Количество пользователей.
        - `n_items`: Количество фильмов.
        - `user_factors`: Матрица разложения содержащая векторы пользователей.
        - `user_items`: Транспонированная матрица разложения, содержащая векторы фильмов.
    - **Магические методы**:
        - `__init__(self, interaction_matrix, n_factors=3, lr=0.01, reg=0.1, n_epochs=3000)`: Инициализирует модель.
    - **Методы**:
        - `train(self)`: Обучает модель.
        - `sgd(self)`: Реализует алгоритм обучения на основе SGD.
        - `predict_single(self, user, item)`: Предсказывает оценку фильма для конкретного пользователя.
        - `predict(self)`: Предсказывает оценки фильмов путем построения обновленной матрицы взаимодействий.
        - `recommend_movies(self, user_id, n_recommendations=10)`: Рекомендует `n_recommendstions` фильмов для пользователя.
        - `calculate_mse(self)`: Вычисляет значение MSE на основе известных и предсказанных данных взаимодействия. 

3. **`Evaluator`**
    - **Описание**: Предоставляет методы для оценки качества обученной модели.
    - **Атрибуты**: 
        - `model`: Обученная модель SVD.
        - `interaction_matrix`: Матрица взаимодействий пользователей и фильмов.
        - `n_users`: Количество пользователей.
        - `n_items`: Количество фильмов.
        - `predict`: Прогнозируемая матрица взаимодействий.
    - **Магические методы**:
        - `__init__(self, model, interaction_matrix)`: Создаёт экземпляр класса.
    - **Методы**:
        - `calculate_rmse(self)`: Вычисляет значение RMSE на основе известных и предсказанных данных взаимодействия. 
        - `calculate_mae(self)`: Вычисляет значение MAE на основе известных и предсказанных данных взаимодействия. 
        - `evaluate(self)`: Оценивает точность модели.

4. **`GUI`**
    - **Описание**: Обеспечивает взаимодействие с пользователем через консольное приложение.
    - **Атрибуты**:
        - `model`: Обученная модель SVDModel для генерации рекомендаций.
        - `movie_data`: Список с информацией о фильмах.
        - `recommendation_count`: Количество фильмов для рекомендации за один запрос.
        - `max_recommendations`: Максимальное количество фильмов для рекомендаций.
        - `user_id`: ID Пользователя.
        - `root`: Главное окно.
        - `label`: Заголовок поля для ввода.
        - `user_id_entry`: Поле для ввода.
        - `recommend_button`: Кнопка для получения рекомендаций.
        - `recommendations_text`: Поле для вывода рекомендаций.
        - `more_button`: Кнопка для добавления рекомендаций.
    - **Магические методы**:
        - `__init__(self, model, movie_data)`: Инициализирует интерфейс с моделью и списком фильмов.
    - **Методы**:
        - `run(self)`: Запускает основное приложение.
        - `show_recommendations(self)`: Отображает первые 10 рекомендаций для введенного ID пользователя.
        - `expand_recommendations(self)`: Расширяет список рекомендаций на 10 фильмов, если это возможно.
        - `display_recommendations(self, recommendations)`: Отображает список рекомендованных фильмов.

## Шаги разработки
1. **Загрузка и обработка данных**
    - Использовать `DataLoader` для загрузки данных.
    - Выполнить обработку и создать матрицу взаимодействий пользователей и фильмов.

2. **Обучение модели**
    - Обучить модель SVD с помощью класса `SVDModel`, используя тренировочные данные.

3. **Оценка модели**
    - Оценить точность модели, используя `Evaluator` и метрики, такие как RMSE и MAE.

4. **Создание пользовательского интерфейса**
    - Реализовать консольный интерфейс с помощью `GUI`, чтобы пользователи могли легко вводить данные и получать рекомендации.
    - Обеспечить обработку ошибок и корректное отображение рекомендаций.

## Инструкция по запуску
В данной инструкции представлен порядок действий для запуска проекта через терминал Windows.
1. Создайте и перейдите в папку проекта:
    - `mkdir <folder_name>`
    - `cd <folder_name>`
2. Создайте и активируйте виртуальную среду разработки: 
    - `python -m venv <env_name>`
    - `<env_name>\Scripts\activate`
3. Инициализируйте пустой репозиторий:
    - `git init`
4. Подключите удаленный репозиторий:
    - `git remote add origin https://github.com/vbobotov/RecommendationSystem2`
    - `git fetch`
5. Перейдите в ветку development:
    - `git checkout origin/development`
6. Установите необходимые зависимости из файла requirements.txt:
    - `pip install -r requirements.txt`
7. Запустите файл main.py:
    - `python src/main.py`
8. Введите ID пользователя во всплывающем окне (в диапозоне от 1 до 9).