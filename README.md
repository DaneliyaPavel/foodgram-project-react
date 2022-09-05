# Проект «Продуктовый помощник» - Foodgram


## Стек технологий

[![Python](https://img.shields.io/badge/-Python-464646?style=flat-square&logo=Python)](https://www.python.org/)
[![Django](https://img.shields.io/badge/-Django-464646?style=flat-square&logo=Django)](https://www.djangoproject.com/)
[![Django REST Framework](https://img.shields.io/badge/-Django%20REST%20Framework-464646?style=flat-square&logo=Django%20REST%20Framework)](https://www.django-rest-framework.org/)
[![PostgreSQL](https://img.shields.io/badge/-PostgreSQL-464646?style=flat-square&logo=PostgreSQL)](https://www.postgresql.org/)
[![Nginx](https://img.shields.io/badge/-NGINX-464646?style=flat-square&logo=NGINX)](https://nginx.org/ru/)
[![gunicorn](https://img.shields.io/badge/-gunicorn-464646?style=flat-square&logo=gunicorn)](https://gunicorn.org/)
[![docker](https://img.shields.io/badge/-Docker-464646?style=flat-square&logo=docker)](https://www.docker.com/)
[![GitHub%20Actions](https://img.shields.io/badge/-GitHub%20Actions-464646?style=flat-square&logo=GitHub%20actions)](https://github.com/features/actions)
[![Yandex.Cloud](https://img.shields.io/badge/-Yandex.Cloud-464646?style=flat-square&logo=Yandex.Cloud)](https://cloud.yandex.ru/)


## Описание
Foodgram - продуктовый помощник. На этом сервисе пользователи смогут публиковать рецепты, подписываться
на публикации других пользователей, добавлять понравившиеся рецепты в список
**«Избранное»**, а перед походом в магазин скачивать сводный список продуктов, необходимых для приготовления одного или нескольких выбранных блюд.

## Инфраструктура
* Проект работает с СУБД PostgreSQL.
* Проект запущен на сервере в Яндекс.Облаке в трёх контейнерах: nginx, PostgreSQL и Django+Gunicorn. Заготовленный контейнер с фронтендом используется для сборки файлов.
* Контейнер с проектом обновляется на Docker Hub.
* В nginx настроена раздача статики, запросы с фронтенда переадресуются в контейнер с Gunicorn. Джанго-админка работает напрямую через Gunicorn.
* Данные сохраняются в volumes.

## Пользовательские роли в проекте
* Анонимный пользователь
* Аутентифицированный пользователь
* Администратор

### Для неавторизованных пользователей
* Доступна главная страница.
* Доступна страница отдельного рецепта.
* Доступна и работает форма авторизации.
* Доступна и работает система восстановления пароля.
* Доступна и работает форма регистрации.

### Для авторизованных пользователей:
* Доступна главная страница.
* Доступна страница другого пользователя.
* Доступна страница отдельного рецепта.
* Доступна страница «Мои подписки».
  1. Можно подписаться и отписаться на странице рецепта.
  2. Можно подписаться и отписаться на странице автора.
  3. При подписке рецепты автора добавляются на страницу «Мои подписки» и удаляются оттуда при отказе от подписки.
* Доступна страница «Избранное».
  1. На странице рецепта есть возможность добавить рецепт в список избранного и удалить его оттуда.
  2. На любой странице со списком рецептов есть возможность добавить рецепт в список избранного и удалить его оттуда.
* Доступна страница «Список покупок».
  1. На странице рецепта есть возможность добавить рецепт в список покупок и удалить его оттуда.
  2. На любой странице со списком рецептов есть возможность добавить рецепт в список покупок и удалить его оттуда.
  3. Есть возможность выгрузить файл (.pdf) с перечнем и количеством необходимых ингредиентов для рецептов из «Списка покупок».
  4. Ингредиенты в выгружаемом списке не повторяются, корректно подсчитывается общее количество для каждого ингредиента.
* Доступна страница «Создать рецепт».
  1. Есть возможность опубликовать свой рецепт.
  2. Есть возможность отредактировать и сохранить изменения в своём рецепте.
  3. Есть возможность удалить свой рецепт.
* Доступна и работает форма изменения пароля.
* Доступна возможность выйти из системы (разлогиниться).

## Установка проекта локально

* Склонировать репозиторий на локальную машину:
```bash
git clone https://github.com/DaneliyaPavel/foodgram-project-react.git
cd foodgram-project-react
```

* Cоздать и активировать виртуальное окружение:

```bash
python -m venv venv
```

```bash
source venv/Scripts/activate
```

* В директории infra создайте файл ```.env``` с переменными окружения для работы с базой данных:
```sh
# ...директория_проекта/infra/.env
# Укажите, что используете postgresql
DB_ENGINE=django.db.backends.postgresql
# Укажите имя созданной базы данных
DB_NAME=postgres
# Укажите имя пользователя
POSTGRES_USER=your_username
# Укажите пароль для пользователя
POSTGRES_PASSWORD=your_pasword
# Укажите db (если будете работать через базу внутри контейнера db), либо ваш IP
DB_HOST=db
# Укажите порт для подключения к базе
DB_PORT=5432
```

* Перейти в директорию и установить зависимости из файла requirements.txt:

```bash
cd backend/
pip install -r requirements.txt
```

* Выставьте в файле settings.py ``DEBUG = True``, для работы локально 
на sqlite3,
или ``DEBUG = False`` для работы с БД PostgeSQL

* Выполните миграции:

```bash
python manage.py makemigrations
python manage.py migrate
```

* Запустите сервер:
```bash
python manage.py runserver
```

## Запуск проекта в Docker контейнере
* Установите Docker.

Параметры запуска описаны в файлах `docker-compose.yml` и `nginx.conf` которые находятся в директории `infra/`.  
При необходимости добавьте/измените адреса проекта в файле `nginx.conf`

* Запустите docker compose:
```bash
docker-compose up -d --build
```  
  > После сборки появляются 3 контейнера:
  > 1. контейнер базы данных **db**
  > 2. контейнер приложения **backend**
  > 3. контейнер web-сервера **nginx**
* Соберите статические файлы (статику):
```
docker-compose exec backend python manage.py collectstatic --no-input
```
* Примените миграции:
```
(опционально) docker-compose exec backend python manage.py makemigrations --noinput
```
```
docker-compose exec backend python manage.py migrate --noinput
```
* Создайте суперпользователя:
```
docker-compose exec backend python manage.py createsuperuser
```
* При необходимости наполните базу тестовыми данными из backend/data/:
```
docker-compose exec backend python manage.py load_ingredients
```
```
docker-compose exec backend python manage.py load_tags
```

## Запуск проекта на сервере
Установите соединение с сервером:
```
ssh your_username@your_server_address
```
Обновите индекс пакетов APT:
```
sudo apt update
```
и обновите установленные в системе пакеты и установите обновления безопасности:
```
sudo apt upgrade -y
```

Скопируйте подготовленные файлы `docker-compose.yml` и `nginx.conf` из вашего проекта на сервер:
```
scp docker-compose.yaml <username>@<host>/home/<username>/docker-compose.yaml
scp nginx.conf <username>@<host>/home/<username>/nginx.conf
```
Установите Docker и Docker-compose:
```
sudo apt install docker.io
```
```
sudo curl -L "https://github.com/docker/compose/releases/download/1.29.2/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
```
```
sudo chmod +x /usr/local/bin/docker-compose
```
Проверьте корректность установки Docker-compose:
```
sudo  docker-compose --version
```
На сервере создайте файл .env 
```
touch .env
```
и заполните переменные окружения
```
nano .env
```
или создайте этот файл локально и скопируйте файл по аналогии с предыдущим шагом. Как создать и заполнять
указано в разделе запуска проекта в Docker контейнере.

> После успешного деплоя выполните все шаги по аналогии с разделом
> **"Запуск проекта в Docker контейнере"**, начиная с шага
> **"Запустите docker compose"**

* Для работы с Workflow добавьте в Secrets GitHub переменные окружения для работы:
    ```
    DB_ENGINE=<django.db.backends.postgresql>
    DB_NAME=<имя базы данных postgres>
    DB_USER=<пользователь бд>
    DB_PASSWORD=<пароль>
    DB_HOST=<db>
    DB_PORT=<5432>
    
    DOCKER_PASSWORD=<пароль от DockerHub>
    DOCKER_USERNAME=<имя пользователя>
    
    SECRET_KEY=<секретный ключ проекта django>
    USER=<username для подключения к серверу>
    HOST=<IP сервера>
    PASSPHRASE=<пароль для сервера, если он установлен>
    SSH_KEY=<ваш SSH ключ (для получения команда: cat ~/.ssh/id_rsa)>
    TELEGRAM_TO=<ID чата, в который придет сообщение>
    TELEGRAM_TOKEN=<токен вашего бота>
    ```
    Workflow состоит из 4 шагов:
     - Проверка кода на соответствие PEP8
     - Сборка и публикация образа бекенда на DockerHub.
     - Автоматический деплой на удаленный сервер.
     - Отправка уведомления в телеграм-чат.  

## Workflow

Main branch status

![main](https://github.com/DaneliyaPavel/foodgram-project-react/workflows/foodgram_project/badge.svg)

## Ссылки
### Адрес развёрнутого проекта:
* Теперь проект доступен по [адресу](http://84.201.135.72/recipes)
* Зайдите на [в админку](http://84.201.135.72/admin/) и убедитесь,
что страница отображается полностью: статика подгрузилась;

## Об авторе
[DaneliyaPavel](https://github.com/DaneliyaPavel)




