## Инструкция по запуску
В данной инструкции представлен порядок действий для запуска проекта через терминал Windows.
1. Создайте и перейдите в папку проекта:
    - `mkdir pythonProject_Bobotov_404`
    - `cd pythonProject_Bobotov_404`
2. Создайте и активируйте виртуальную среду разработки: 
    - `python -m venv venv`
    - `venv\Scripts\activate`
3. Клонируйте репозиторий с GitHub:
    - `git clone https://github.com/vbobotov/RecommendationSystem2`
4. Перейдите в ветку development:
    - `git checkout development`
5. Установите необходимые зависимости из файла requirements.txt:
    - `pip install -r requirements.txt`
6. Запустите файл main.py:
    - `python main.py`
7. Введите ID пользователя во всплывающем окне (в диапозоне от 1 до 9).