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
# Redis
REDIS_HOST=localhost
REDIS_USER=admin
REDIS_PASSWORD=admin
REDIS_PORT=6379 or SSL 6380

# PostgreSQL
PSQL_NAME=dp_prom
PSQL_USER=admin
PSQL_PASSWORD=admin
PSQL_HOST=localhost
PSQL_PORT=5432
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