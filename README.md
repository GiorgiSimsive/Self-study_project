# 📚 Платформа для самообучения студентов

Проект дипломной работы: REST API для платформы с курсами, материалами и тестами.  
Реализованы авторизация, роли пользователей, CRUD для всех сущностей и проверка ответов на тесты.

## 🚀 Стек технологий
- **Backend:** Django 5, Django Rest Framework
- **Auth:** JWT (SimpleJWT)
- **БД:** PostgreSQL
- **Документация:** drf-spectacular (Swagger, ReDoc)
- **Тесты:** pytest + pytest-django
- **Стиль кода:** PEP8, flake8, black, isort
- **Безопасность:** django-cors-headers

---

## 📂 Структура проекта
project/
│ README.md
│ .env.example
│ manage.py
│ pyproject.toml
│
├─ config/ # настройки Django
├─ users/ # приложение пользователей
├─ courses/ # курсы, материалы, тесты
├─ tests/ # тесты pytest
└─ docs/ # документация OpenAPI

---

## 🔧 Установка и запуск

### 
1. Клонируем репозиторий
git clone git@github.com:GiorgiSimsive/Self-study_project.git
cd self-study-project
2
2. Устанавливаем зависимости
poetry install
3. Настраиваем окружение
Создаём .env из примера:
cp .env.example .env
Правим переменные под свою БД.
4. Применяем миграции и создаём суперпользователя
poetry run python manage.py migrate
poetry run python manage.py createsuperuser
5. Запуск сервера
poetry run python manage.py runserver

## 🔑 Роли пользователей
Роль	Возможности
admin	Полный доступ ко всем функциям
teacher	CRUD только для своих курсов, материалов, тестов
student	Только просмотр и прохождение тестов

Тестовые пользователи можно создать через команду:

poetry run python manage.py seed_data
Логины/пароли будут выведены в консоль.

## 📜 Документация API
Swagger UI — http://127.0.0.1:8000/api/docs/

ReDoc — http://127.0.0.1:8000/api/redoc/

OpenAPI JSON — http://127.0.0.1:8000/api/schema/

## 🧪 Тестирование
Запуск всех тестов:
poetry run pytest -q

## 🔌 Основные эндпоинты
Метод	URL	Описание
POST	/api/register/	Регистрация
POST	/api/token/	Получить токен
GET	/api/courses/	Список курсов
GET	/api/tests/{id}/full/	Тест с вопросами и ответами
POST	/api/tests/submit/	Отправить ответы

## 📦 Переменные окружения
См. .env.example

```env
SECRET_KEY=supersecretkey
DEBUG=1
ALLOWED_HOSTS=127.0.0.1,localhost

DB_NAME=project_db
DB_USER=postgres
DB_PASSWORD=yourpassword
DB_HOST=localhost
DB_PORT=5432

CORS_ORIGINS=http://localhost:3000,http://127.0.0.1:3000