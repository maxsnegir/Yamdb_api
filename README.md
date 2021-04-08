# Проект "Yamdb"
### Описание
Проект YaMDb собирает отзывы пользователей на произведения, которые делятся на категории.
Благодарные или возмущённые читатели оставляют к произведениям текстовые отзывы и выставляют произведению рейтинг (оценку в диапазоне от одного до десяти). 
Из множества оценок автоматически высчитывается средняя оценка произведения.

### Технологии
- Python 3.8
- Django 3.0.5
- djangorestframework 3.11.0
- Postgres 12
- Docker 
- Nginx 1.19.3

### Запуск проекта
_Все команды должны выполняться в главной директории проекта._

- Создайте файл .env с переменными окружения для работы с базой данных:
  DB_ENGINE=django.db.backends.postgresql # указываем, что работаем с postgresql
  DB_NAME=postgres # имя базы данных
  POSTGRES_USER=postgres # логин для подключения к базе данных
  POSTGRES_PASSWORD=postgres # пароль для подключения к БД (установите свой)
  DB_HOST=db # название сервиса (контейнера)
  DB_PORT=5432 # порт для подключения к БД 

- Запустите проект следующей командой:
- ```docker-compose up ```
– Проект запущен и доступен по адресу http://127.0.0.1

- Чтобы выполнить миграции, собрать статические файлы и создать суперпользователя, выполните:
- ```docker-compose exec web python manage.py migrate --noinput```
- ```docker-compose exec web python manage.py createsuperuser```
- ```docker-compose exec web python manage.py collectstatic --no-input```

- Чтобы заполнить базу тестовыми данными, выполните команду:
- ```docker-compose exec web python manage.py loaddata fixtures.json```




