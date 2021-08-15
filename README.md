### Описание проекта:

Проект YaMDb собирает отзывы пользователей на различные произведения.

### Как запустить проект:

Клонировать репозиторий и перейти в него в командной строке:

```
git clone git@github.com:ikazman/api_yamdb.git
```

```
cd api_yamdb
```

Cоздать и активировать виртуальное окружение:

```
python3 -m venv env
```

```
source venv/bin/activate
```

Установить зависимости из файла requirements.txt:

```
python3 -m pip install --upgrade pip
```

```
pip install -r requirements.txt
```

Подготовить и выполнить миграции:

```
python3 manage.py makemigrations
```
```
python3 manage.py migrate
```
Запустить базу данных из csv:

```
python3 manage.py load_data --path static/data
```
Запустить проект:

```
python3 manage.py runserver
```
### Документация к api:
http://127.0.0.1:8000/redoc/

### Примеры запросов:

- регистрация нового пользователя:
http://127.0.0.1:8000/api/v1/auth/signup/

- получение JWT-токена:
http://127.0.0.1:8000/api/v1/auth/token/

- получение списка всех произведений:
http://127.0.0.1:8000/api/v1/titles/

- получение списка всех отзывов:
http://127.0.0.1:8000/api/v1/titles/{title_id}/reviews/
