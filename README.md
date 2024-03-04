# backend

## Запуск проекта

**Требования**

Установлен docker, docker-compose, установлена десктопная версия докера если 
windows.
После клонирования репы, нужно создать новые `.env` на уровне с `.env.example`,
либо переименовать.
Находятся они в:
1. `/backend/.env.example`
2. `/backend/infra/.env.example`

#### Build
path
```
/backend/infra
```
command start
```python
docker-compose up -d --build
```
command stop
```python
docker-compose down -v
```

#### Endpoints

1. [localhost/login/]() - авторизация
2. [localhost/api/v1/users/]() - возвращает Имя/Фамилия менеджера
3. [localhost/api/docs/]() - SWAGGER
