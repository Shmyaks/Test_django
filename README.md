## Как запустить
1. Клонируйте репозиторий.
2. `python manage.py makemigrations`
3. `python manage.py migrate`
4. `python manage.py createsuperuser`
4. `docker-compose build`
5. `docker-compose up`
## Тестирование и маршруты
- Swagger - http://localhost:8000/swagger/docs/
- Tests - `python manage.py test` (Во время работы веб приложения). Создаём небольшую базу.
