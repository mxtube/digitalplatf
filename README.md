# Digital Platform

Digital Platform - это платформа для образовательных организаций предназначенная автоматизировать учебный процесс. Она предоставляет функционал:
1. Предоставление расписания занятий
2. Заказ справок

Digital Platform написана на Python и Django и использует базу данных SQL для хранения данные.

# Установка
После клонирования репозитория, установите виртуальное окружение, активируйте виртуальное окружение и установите библиотеки из файла requirements.txt
```text
pip install -r requirements.txt
```


# Debug

Parsing
```python
import datetime
from schedule_parsing.parsing import Parsing
parse = Parsing(filename='FridayEven.xlsx', department='ЦИКТ', date=datetime.date.today())
print(parse.parse())
```