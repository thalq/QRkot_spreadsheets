# QRKot

## Описание проекта

**QRkot** - это API сервиса по сбору средств для финансирования благотворительных проектов. В сервисе реализована возможность регистрации пользователей, добавления благотворительных проектов и пожертвований, которые распределяются по открытым проектам.

Настроено автоматическое создание первого суперпользователя при запуске проекта.

Реализована возможность получить отчет с перечнем профинансированных проектов, отсортированных по времени, потребовавшимся для полного закрытия.

## Ключевые технологии и библиотеки:
- [Python](https://www.python.org/);
- [FastAPI](https://fastapi.tiangolo.com/);
- [SQLAlchemy](https://pypi.org/project/SQLAlchemy/);
- [Alembic](https://pypi.org/project/alembic/);
- [Pydantic](https://pypi.org/project/pydantic/);
- [Asyncio](https://docs.python.org/3/library/asyncio.html);
- [Google Sheets](https://www.google.ru/intl/ru/sheets/about/);

## Установка
1. Склонируйте репозиторий:
```
git clone git@github.com:thalq/cat_charity_fund.git
```
2. Активируйте venv и установите зависимости:

```
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```
3. Создайте в корневой директории файл .env со следующим наполнением:

```
APP_TITLE=Кошачий благотворительный фонд
APP_DESCRIPTION=Сервис для поддержки котиков
DATABASE_URL=sqlite+aiosqlite:///./<название базы данных>.db
SECRET=<секретное слово>
FIRST_SUPERUSER_EMAIL=<email суперюзера>
FIRST_SUPERUSER_PASSWORD=<пароль суперюзера>

Данные, получаемые после настройки Google Cloud:
TYPE=service_account
PROJECT_ID=atomic-climate-<идентификатор>
PRIVATE_KEY_ID=<id приватного ключа>
PRIVATE_KEY="-----BEGIN PRIVATE KEY-----<приватный ключ>-----END PRIVATE KEY-----\n"
CLIENT_EMAIL=<email сервисного аккаунта>
CLIENT_ID=<id сервисного аккаунта>
AUTH_URI=https://accounts.google.com/o/oauth2/auth
TOKEN_URI=https://oauth2.googleapis.com/token
AUTH_PROVIDER_X509_CERT_URL=https://www.googleapis.com/oauth2/v1/certs
CLIENT_X509_CERT_URL=<ссылка>
EMAIL=<email пользователя>
```
4. Примените миграции для создания базы данных SQLite:
```
alembic upgrade head
```
5. Проект готов к запуску.

## Управление:
Для локального запуска выполните команду:
```
uvicorn app.main:app --reload
```
Сервис будет запущен и доступен по следующим адресам:
- http://127.0.0.1:8000 - API
- http://127.0.0.1:8000/docs - автоматически сгенерированная документация Swagger
- http://127.0.0.1:8000/redoc - автоматически сгенерированная документация ReDoc

После запуска доступны следующие эндпоинты:
- Регистрация и аутентификация:
    - **/auth/register** - регистрация пользователя
    - **/auth/jwt/login** - аутентификация пользователя (получение jwt-токена)
    - **/auth/jwt/logout** - выход (сброс jwt-токена)
- Пользователи:
    - **/users/me** - получение и изменение данных аутентифицированного пользователя
    - **/users/{id}** - получение и изменение данных пользователя по id
- Благотворительные проекты:
    - **/charity_project/** - получение списка проектов и создание нового
    - **/charity_project/{project_id}** - изменение и удаление существующего проекта
- Пожертвования:
    - **/donation/** - получение списка всех пожертвований и создание пожертвования
    - **/donation/my** - получение списка всех пожертвований аутентифицированного пользователя
- Отчеты Google Sheets:
    - **/google** - получение отчета о закрытых (профинансированных) проектах в формате Google Sheets. Отчет создается в указанном в .env личном аккаунте Google.

Со схемами запросов и ответов можно ознакомиться в документации или в файле со спецификацией - openapi.json.


### Автор
[Tanya Khalkvist](https://github.com/thalq)
