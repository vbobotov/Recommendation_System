# Система рекомендаций фильмов

Этот проект на Python предназначен для создания простой системы рекомендаций фильмов с использованием коллаборативной фильтрации. Цель проекта — предсказать, какие фильмы могут понравиться пользователю, основываясь на его предыдущих оценках и оценках других пользователей. Система использует датасет Netflix Prize и алгоритм SVD (сингулярное разложение) для генерации рекомендаций.

## Оглавление
- [Описание проекта](#описание-проекта)
- [Архитектура проекта](#архитектура-проекта)
- [Шаги разработки](#шаги-разработки)

## Описание проекта
Этот проект демонстрирует основы коллаборативной фильтрации, с акцентом на создание модульного дизайна, вдохновленного популярными библиотеками для рекомендательных систем, такими как Surprise. Система использует item-based коллаборативную фильтрацию с алгоритмом SVD, чтобы выявлять скрытые паттерны предпочтений пользователей. Она спроектирована так, чтобы быть простой, но эффективной, и подходит для начинающих, которые хотят научиться работать с рекомендательными системами и машинным обучением.

## Архитектура проекта
Проект структурирован на несколько модульных компонентов, каждый из которых представлен отдельным классом для улучшения читаемости и поддержки кода. Ниже описаны основные классы и их обязанности:

### Классы
1. **`DataLoader`**
    - **Описание**: Отвечает за загрузку данных об оценках и информации о фильмах из файлов.
    - **Атрибуты**: 
        - `ratings_file`: Путь к CSV файлу с оценками пользователей.
        - `movies_file`: Путь к CSV файлу с информацией о фильмах.
    - **Магические методы**:
        - `__init__(self, ratings_file, movies_file)`: Инициализирует пути к файлам.
        - `__repr__(self)`: Возвращает строковое представление класса, показывающее, какие файлы будут загружены.
    - **Методы**:
        - `load_ratings(self)`: Загружает данные об оценках пользователей из файла и преобразует их в формат DataFrame.
        - `load_movies(self)`: Загружает данные о фильмах, такие как названия, жанры и год выпуска.
        - `preprocess_data(self)`: Выполняет очистку данных, удаляет пропуски и проводит базовую нормализацию.

2. **`Preprocessor`**
    - **Описание**: Отвечает за создание матрицы взаимодействий и нормализацию данных для подготовки их к обучению модели.
    - **Атрибуты**: 
        - `ratings_data`: DataFrame с оценками пользователей.
        - `movies_data`: DataFrame с информацией о фильмах.
        - `user_item_matrix`: Матрица взаимодействий пользователей и фильмов.
        - `normalized_matrix`: Нормализованная версия матрицы взаимодействий.
        - `user_means`: Словарь, где ключами являются ID пользователей, а значениями — средние оценки.
        - `movie_ids`: Список ID фильмов, доступных для рекомендаций.
    - **Магические методы**:
        - `__init__(self, ratings_data, movies_data=None)`: Инициализирует данные об оценках и фильмы.
        - `__repr__(self)`: Возвращает строковое представление с количеством пользователей и фильмов в данных.
    - **Методы**:
        - `create_user_item_matrix(self)`: Создаёт матрицу взаимодействий.
        - `normalize_data(self)`: Выполняет нормализацию данных.

3. **`SVDModel`**
    - **Описание**: Реализует алгоритм SVD для предсказания оценок фильмов и генерации рекомендаций.
    - **Атрибуты**:
        - `n_factors`: Количество скрытых факторов для разложения SVD.
        - `model`: Обученная модель SVD.
    - **Магические методы**:
        - `__init__(self, n_factors=50)`: Инициализирует модель с заданным количеством скрытых факторов.
        - `__repr__(self)`: Возвращает строковое представление модели с числом факторов.
    - **Методы**:
        - `train(self, train_data)`: Обучает модель на основе матрицы взаимодействий.
        - `predict(self, user_id, movie_id)`: Предсказывает оценку фильма для конкретного пользователя.
        - `recommend(self, user_id, n)`: Рекомендует `n` фильмов для пользователя.

4. **`Evaluator`**
    - **Описание**: Предоставляет методы для оценки качества обученной модели.
    - **Атрибуты**: Отсутствуют.
    - **Магические методы**:
        - `__init__(self)`: Создаёт экземпляр класса.
        - `__repr__(self)`: Возвращает строку, указывающую на функции оценки.
    - **Методы**:
        - `evaluate_model(self, predictions)`: Оценивает точность модели.
        - `cross_validate(self, data, folds=5)`: Выполняет кросс-валидацию.

5. **`AppInterface`**
    - **Описание**: Обеспечивает взаимодействие с пользователем через консольное приложение.
    - **Атрибуты**:
        - `available_movies`: Список ID фильмов, доступных для рекомендации.
        - `user_prompt`: Текст приветствия и инструкции для пользователя.
        - `error_message`: Сообщение об ошибке в случае неверного ввода.
        - `recommendation_count`: Количество фильмов для рекомендаций.
    - **Магические методы**:
        - `__init__(self, model, available_movies)`: Инициализирует интерфейс с моделью и списком доступных фильмов.
        - `__repr__(self)`: Возвращает строковое представление, показывающее количество доступных фильмов и статус модели.
    - **Методы**:
        - `run(self)`: Запускает основное приложение.
        - `get_user_input(self)`: Запрашивает ID пользователя через консоль и обрабатывает ввод.
        - `display_recommendations(self, recommendations)`: Отображает список рекомендованных фильмов.
        - `display_error(self)`: Выводит сообщение об ошибке.

## Шаги разработки
1. **Загрузка и исследование данных**
    - Использовать `DataLoader` для загрузки данных и предварительного исследования.
    - Выполнить очистку и подготовку данных для дальнейшего анализа.

2. **Предобработка данных**
    - Создать матрицу взаимодействий пользователей и фильмов с помощью класса `Preprocessor`.
    - Провести нормализацию, чтобы устранить смещения в оценках пользователей.

3. **Обучение модели**
    - Обучить модель SVD с помощью класса `SVDModel`, используя тренировочные данные.
    - Настроить гиперпараметры, применив кросс-валидацию.

4. **Оценка модели**
    - Оценить точность модели, используя `Evaluator` и метрики, такие как RMSE и MAE.
    - Проверить устойчивость модели на тестовых данных.

5. **Создание пользовательского интерфейса**
    - Реализовать консольный интерфейс с помощью `AppInterface`, чтобы пользователи могли легко вводить данные и получать рекомендации.
    - Обеспечить обработку ошибок и корректное отображение рекомендаций.
