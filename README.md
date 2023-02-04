# Yatube

## Описание
Данный проект представляет собой  портал на котором авторы выкладывают посты на интересующую их тематику.

Имеется возможность прикладывать изображения к постам.

Пользователи могут комментировать  статьи, и подписываться на понравившихся авторов.

Реализована авторизация через email. Проект покрыт тестами.

Данный проект создавался в учебных целях при изучении Django ORM и HTML.


## Как запустить проект:

Клонировать репозиторий и перейти в него в командной строке:

```
git clone https://github.com/Algor45/hw05_final.git
```

```
cd hw05_final/
```

Cоздать и активировать виртуальное окружение:

```
py -3.7 -m venv env
```

```
source venv/bin/activate
```

Установить зависимости из файла requirements.txt:

```
py -m pip install --upgrade pip
```

```
pip install -r requirements.txt
```

Перед использованием сгенерируйте новый секретный ключ
и укажите его в файле:

```
yatube/yatube/settings.py

SECRET_KEY='Ваш ключ'

для генерации ключа можно использовать сайт:

https://djecrety.ir/
```


Перейти в папку, в которой находится файл manage.py:

```
cd yatube/
```

Выполнить миграции:

```
python manage.py migrate
```

Запустить проект:

```
python manage.py runserver
```


## Системные требования

Версия Python:

```
Python 3.7
```

Зависимости:

```
atomicwrites==1.4.1
attrs==22.1.0
certifi==2022.6.15
charset-normalizer==2.0.12
colorama==0.4.5
Django==2.2.16
django-debug-toolbar==3.2.4
Faker==12.0.1
flake8==5.0.4
idna==3.3
importlib-metadata==4.2.0
iniconfig==1.1.1
isort==5.10.1
mccabe==0.7.0
mixer==7.1.2
packaging==21.3
Pillow==8.3.1
pluggy==0.13.1
py==1.11.0
pycodestyle==2.9.1
pydocstyle==6.1.1
pyflakes==2.5.0
pyparsing==3.0.9
pytest==6.2.4
pytest-django==4.4.0
pytest-pythonpath==0.7.3
python-dateutil==2.8.2
python-dotenv==0.21.1
pytz==2022.2.1
requests==2.26.0
six==1.16.0
snowballstemmer==2.2.0
sorl-thumbnail==12.7.0
sqlparse==0.4.2
toml==0.10.2
typing_extensions==4.3.0
urllib3==1.26.12
zipp==3.8.1
```
