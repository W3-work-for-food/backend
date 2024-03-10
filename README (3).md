
# Backend REST API сервис для CRM Амбассадоры Яндекса на базе Python, Django и Django REST Framework.

### Описание проекта

**CRM для «Амбассадоры Практикума»**

**Сервис:**

* Управление взаимодействием с амбассадорами «Яндекс Практикума».
* API для взаимодействия с фронтендом CRM.

**Функционал:**

* Регистрация и авторизация.
* Хранение и управление данными о амбассадорах.
* Отслеживание активности, мерча, затрат.
* FAQ и уведомления.
 - - - - - - - - - - - - - - - - - - - - - - - -

### Используемый стек<a name="stack"></a>

[![Python][Python-badge]][Python-url]
[![Django][Django-badge]][Django-url]
[![DRF][DRF-badge]][DRF-url]
[![Python-telegram-bot][Python-telegram-bot-badge]][Python-telegram-bot-url]
[![Postgres][Postgres-badge]][Postgres-url]
[![Nginx][Nginx-badge]][Nginx-url]

* Python 3.11.0
* PDjango 4.2
* djangorestframework 3.14.0
 - - - - - - - - - - - - - - - - - - - - - - - -

### 📋 Требования

- Установленный [Docker](https://www.docker.com/products/docker-desktop) и Docker Compose
- Для Windows требуется десктопная версия Docker
- - - - - - - - - - - - - - - - - - - - - - - -

### ⚙️ Настройка окружения

1. Клонируйте репозиторий
```bash
git clone https://github.com/Studio-Yandex-Practicum/you_can_bot.git && cd you_can_bot
```
2. Создайте `.env` файлы на основе `.env.example`:
    - `/backend/.env.example`
    - `/backend/infra/.env.example`
- - - - - - - - - - - - - - - - - - - - - - - -

### 🏗 Сборка и Запуск

Перейдите в директорию инфраструктуры и выполните команды:

```bash
cd /backend/infra
docker-compose up -d --build
```

Cоздать суперпользователя для входа в Админку:

```bash
docker compose -f docker-compose.local.yml exec -it backend python manage.py createsuperuser
```

После этого Админка должна стать доступна по адресу: http://localhost/admin/
API Root будет доступен по адресу: http://localhost/api/


Для остановки и удаления контейнеров используйте

```bash
docker-compose down -v
```
- - - - - - - - - - - - - - - - - - - - - - - -
#### Endpoints

* Авторизация
```bash
[localhost/login/]()
```
* Пользователи
```bash
[localhost/api/v1/users/]()
```
* SWAGGER документация API
```bash
[localhost/api/docs/]()
```


<!-- MARKDOWN LINKS & BADGES -->

[Python-url]: https://www.python.org/

[Python-badge]: https://img.shields.io/badge/Python-376f9f?style=for-the-badge&logo=python&logoColor=white

[Django-url]: https://github.com/django/django

[Django-badge]: https://img.shields.io/badge/Django-0c4b33?style=for-the-badge&logo=django&logoColor=white

[DRF-url]: https://github.com/encode/django-rest-framework

[DRF-badge]: https://img.shields.io/badge/DRF-a30000?style=for-the-badge

[Python-telegram-bot-url]: https://github.com/python-telegram-bot/python-telegram-bot

[Python-telegram-bot-badge]: https://img.shields.io/badge/python--telegram--bot-4b8bbe?style=for-the-badge

[Postgres-url]: https://www.postgresql.org/

[Postgres-badge]: https://img.shields.io/badge/postgres-306189?style=for-the-badge&logo=postgresql&logoColor=white

[Nginx-url]: https://nginx.org

[Nginx-badge]: https://img.shields.io/badge/nginx-009900?style=for-the-badge&logo=nginx&logoColor=white