# Blogs App
**[Русский](#russian-version) | [English](#english-version)**

## Russian version
Веб-приложение на Flask для управления блогами с авторизацией, задачами и категориями постов.

### Возможности
- **Регистрация и авторизация**: Создание учетных записей, вход и выход из системы.
- **Посты**: Добавление, редактирование и удаление постов с поддержкой публичного/приватного доступа.
- **Задачи**: Управление личными задачами (название, объем работы, участники, статус завершения).
- **Категории**: Классификация постов по категориям для удобной организации контента.

### Установка
1. Склонируйте репозиторий:
    ```
    git clone https://github.com/FedotovSvyatoslav/blogs_app
    ```
2. Установите зависимости:
    ```
    pip install -r requirements.txt
    ```
3. Запустите приложение:
    ```
    python app.py
    ```

Укажите путь к базе данных, например, `db/blogs.db`, когда будет предложено.

### Управление
- **Общее**: Переход между страницами через панель навигации.
- **Посты**: Кнопки "Добавить новость", "Изменить", "Удалить" на главной странице.
- **Задачи**: Управление через раздел "Tasks".
- **Категории**: Добавление новых категорий в разделе "Categories".

### Особенности
- Модульная структура с использованием Flask и SQLAlchemy.
- Поддержка SQLite для хранения данных о пользователях, постах, задачах и категориях.
- Интерфейс на основе Bootstrap для аккуратного дизайна.
- Отношения многие-ко-многим между постами и категориями.

### Структура проекта
- `data/`: Модели базы данных (`User`, `News`, `Jobs`, `Category`) и управление сессиями.
- `db/`: Файлы SQLite базы данных (например, `blogs.db`).
- `templates/`: HTML-шаблоны с использованием Bootstrap.
- `app.py`: Основной файл приложения.
- `requirements.txt`: Список зависимостей.


### Автор
- [Федотов Святослав](https://github.com/FedotovSvyatoslav)

---

## English Version
A Flask-based web application for managing blogs with authentication, tasks, and post categories.

### Features
- **Registration and Authentication**: Create accounts, log in, and log out.
- **Posts**: Add, edit, and delete posts with public/private visibility.
- **Tasks**: Manage personal tasks (title, work size, collaborators, completion status).
- **Categories**: Categorize posts for better content organization.

### Installation
1. Clone the repository:
    ```
    git clone https://github.com/FedotovSvyatoslav/blogs_app
    ```
2. Install dependencies:
    ```
    pip install -r requirements.txt
    ```
3. Run the application:
    ```
    python app.py
    ```

Enter the database path, e.g., `db/blogs.db`, when prompted.

### Controls
- **General**: Navigate using the top navigation bar.
- **Posts**: Use "Add News", "Edit", and "Delete" buttons on the main page.
- **Tasks**: Manage via the "Tasks" section (click-based interface).
- **Categories**: Add new categories in the "Categories" section.

### Features
- Modular structure using Flask and SQLAlchemy.
- SQLite support for storing users, posts, tasks, and categories.
- Bootstrap-based interface for a clean design.
- Many-to-many relationship between posts and categories.

### Project Structure
- `data/`: Database models (`User`, `News`, `Jobs`, `Category`) and session management.
- `db/`: SQLite database files (e.g., `blogs.db`).
- `templates/`: HTML templates with Bootstrap.
- `app.py`: Main application file.
- `requirements.txt`: List of dependencies.

