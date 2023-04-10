![example workflow](https://github.com/AnnaMolodova/foodgram-project-react/actions/workflows/foodgram_workflow.yml/badge.svg)
# 51.250.80.139 (в данное время сервер отключен в целях экономии)
# Сайт Foodgam - Продуктовый помощник

## _Сервис для публикации рецептов_


На этом сервисе пользователи смогут публиковать рецепты, подписываться на публикации других пользователей, добавлять понравившиеся рецепты в список «Избранное», а перед походом в магазин скачивать сводный список продуктов, необходимых для приготовления одного или нескольких выбранных блюд.

## Стек технологий:
- Python
- Django
- PostgreSQL
- Docker
- Docker-compose
- React
- CI/CD


Структура проекта:
- В папке frontend находятся файлы, необходимые для сборки фронтенда приложения
- В папке infra — конфигурационный файл nginx и docker-compose.yml
- В папке backend — файлы для сборки бекенд приложения
- В папке data подготовлен список ингредиентов с единицами измерения
- В папке docs — файлы спецификации API, по которым работает проект

## Посмотреть API в Redoc:
Необходимо запустить проект локально и перейти по ссылке: http://localhost/api/docs/

## Локальный запуск проекта в контейнерах:

- Склонировать репозиторий к себе на компьютер и перейти в корневую папку
```sh
git clone git@github.com:AnnaMolodova/foodgram-project-react.git
```
```sh
cd foodgram-project-react
```
- Создать файл .env с переменными окружения, необходимыми для работы

> DB_ENGINE=django.db.backends.postgresql

> DB_NAME=postgres

> POSTGRES_USER=postgres

> POSTGRES_PASSWORD=postgres

> DB_HOST=db

> DB_PORT=5432

> SECRET_KEY=postgres

- Перейти в папку /infra и запустить сборку контейнеров (запущены контейнеры db, backend, nginx)
```sh
docker-compose up -d
```
- Внутри контейнера backend выполнить миграции, создать суперюзера, собрать статику и загрузить ингредиенты и теги
```sh
docker-compose exec backend python manage.py migrate
```
```sh
docker-compose exec backend python manage.py createsuperuser
```
```sh
docker-compose exec backend python manage.py collectstatic --no-input
```
```sh
docker-compose exec backend python manage.py fromcsv_ingred
```
```sh
docker-compose exec backend python manage.py fromcsv_tags
```
### _Проект будет доступен по адресу:  http://localhost/_
- Для остановки приложения в терминале зажать ctrl+с
- Для повторного запуска без пересборок в папке /infra использовать команду:
```sh
docker-compose start
```
Автор: Молодова Анна
