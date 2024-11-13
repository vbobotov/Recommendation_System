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