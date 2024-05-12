# Digital Platform

Digital Platform - это платформа для образовательных организаций предназначенная автоматизировать учебный процесс. Она предоставляет функционал:
1. Предоставление расписания занятий
2. Заказ справок

Digital Platform написана на Python и Django и использует базу данных PostgreSQL для хранения данные.

---
# Установка
Скачайте файлы проекта, установите виртуальное окружение в папке src. Установите библиотеки из файла requirements.txt
```text
pip install -r requirements.txt
```

Для работы приложения разверните Redis и PostgreSQL, создайте файл .env в папке dpapp и укажите значения:
```shell
# Project
DJANGO_SECRET_KEY=''
DEBUG=1

# Redis
REDIS_HOST=''
REDIS_USER=''
REDIS_PASSWORD=''
REDIS_PORT=6379

# Postgres
POSTGRES_DB=''
POSTGRES_USER=''
POSTGRES_PASSWORD=''
POSTGRES_HOST=127.0.0.1
POSTGRES_PORT=5432

# Email
EMAIL_HOST='smtp.yandex.ru'
EMAIL_HOST_USER=''
EMAIL_HOST_PASSWORD=''
EMAIL_PORT=465
EMAIL_USE_TLS=0
EMAIL_USE_SSL=1
```

В корне проекта запустите docker compose
```shell
./docker_run.sh
```

Мигруруйте базу данных

### Тестовые данные
Для загрузки демо данных используйте файл run.sh в директории src.

### Deploy
Сгенерируй новый секретный ключ и положи в .env:
```dotenv
DJANGO_SECRET_KEY=<key>
```

```python
from django.core.management.utils import get_random_secret_key
print(get_random_secret_key())
```




---
# Dev Debug
### CSS/Sass
Для работы с препроцессором CSS используйте программу [Prepros](https://prepros.io). Сборка статических файлов осуществляется с помощью команды:
```text
./manage.py collectstatic --no-input -i sass
```

### Parsing
```python
import datetime
from schedule_parsing.parsing import Parsing
parse = Parsing(filename='FridayEven.xlsx', department='ЦИКТ', date=datetime.date.today())
print(parse.parse())
```

### Dumpdata
Для экспорта данных используйте команду:
```text
./manage.py dumpdata educationpart.studygroup --format=yaml > <name>.yaml
./manage.py dumpdata educationpart.studygroup > <name>.json
```