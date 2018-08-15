# Установка необходимых библиотек:
``pip install -r requirements.txt``


# Запуск
```
./manage.py test
./manage.py migrate
./manage.py runserver
```

# Интерактивная документация API (Swagger)
http://localhost:8000/api/docs

# Документация API

## Регистрация
**POST /api/sign_up/**
```
{
  "username": "tester",
  "email": "tester@test.ru",
  "password": "password",
  "password_2": "password"
}
```
* email не обязателен
* password и password_2 должны совпадать

**Response**:
```
{
  "id": 4,
  "username": "tester",
  "email": "tester@test.ru"
}
```

## Авторизация

Авторизация реализована с помощью JWT, т.е. пользователь хранит 2 токена: refresh и access. С access токеном идентифицируется юзер на бэкенде. C refresh токеном обновляет access токен.

Время жизни access токена **10 минут**

**POST /api/token/**
```
{
  "username": "newtester",
  "password": "123qwe123"
}
```
**Response**
```
{
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTUzNDQwMjM3MCwianRpIjoiMzQxMjBmY2NmZGIyNGUwNTg3NzU5YzcwMjUzNjMzZDgiLCJ1c2VyX2lkIjo1fQ.gvaSTZO0_efIR6ltYzCt4KmId8IU_wRXlAZcq6dlC28",
  "access": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNTM0MzE2NTcwLCJqdGkiOiJiNmEwMWRhODBiNzg0OWZkOTFmMTJkMzJhMTE3MjZkZiIsInVzZXJfaWQiOjV9.HJAaI9G1eQqVFiQgu0EDfdqZzbThzeFtt5-WZXajeqQ"
}
```
**POST /api/token/refresh/**
```
{
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTUzNDQwMjM3MCwianRpIjoiMzQxMjBmY2NmZGIyNGUwNTg3NzU5YzcwMjUzNjMzZDgiLCJ1c2VyX2lkIjo1fQ.gvaSTZO0_efIR6ltYzCt4KmId8IU_wRXlAZcq6dlC28"
}
```
**Response**
```
{
  "access": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNTM0MzE2NzA2LCJqdGkiOiJhZmM4MWQ3N2EzYWQ0ZDA3ODk3ZWExNDNjY2Y1ZjdjMCIsInVzZXJfaWQiOjV9.iZcXSHShOpfyJVBkDLjthwu-qA7yMTERR6wFsn42H6g",
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTUzNDQwMjUwNiwianRpIjoiZGFlMjNmYzA3ZmE0NDNlMmIxNzZlMjIzMGU1NzBlMDEiLCJ1c2VyX2lkIjo1fQ.2Sq4VhnztgfuMeKwmS7TaP4nRBHO2_1kvRgw4uoElSM"
}
```
**POST /api/token/verify/**
_verify access token_
```
{
  "token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNTM0MzE2NzA2LCJqdGkiOiJhZmM4MWQ3N2EzYWQ0ZDA3ODk3ZWExNDNjY2Y1ZjdjMCIsInVzZXJfaWQiOjV9.iZcXSHShOpfyJVBkDLjthwu-qA7yMTERR6wFsn42H6g"
}
```
**Response 200**
```
{}
```

## Профиль
Получить информацию о текущем пользователе (определяется по access токену).
**GET /api/profile/**
```
{
  "id": 4,
  "username": "tester",
  "email": "tester@test.ru"
}
```

## Публикации

Объект **Post**:
* id - int
* user - object User
* created_at - str datetime ("2018-08-15T05:20:38.770056Z")
* text - text
* likes_count - int
* likes - array of objects Like
* media_files - array of objects MediaFile
* links - array of objects Link

Объект **User**:
* id - int
* username - str
* email - str

Объект **Like**:
* user - object User
* created_at - str datetime
* updated_at - str datetime
* post - int

Объект **MediaFile**:
* id - int
* file - str url
* filename - str
* post - int

Объект **Link**:
* id - int
* link - str url
* title - str / null
* desc - str / null
* image - str url / null
* post - id

**GET /api/posts/**
Получение списка постов с пагинацией
Параметры:
* page - integer
* page_size - integer (default: 10)

Example: http://localhost:8000/api/posts/?page_size=1&page=1
**Response Example**
```
{
  "count": 45,
  "next": "http://localhost:8000/api/posts/?page=2&page_size=1",
  "previous": null,
  "results": [
    {
      "id": 46,
      "user": {
        "id": 3,
        "username": "soapyhead",
        "email": "rta@tigrio.ru"
      },
      "likes_count": 0,
      "likes": [],
      "media_files": [
        {
          "id": 16,
          "file": "http://localhost:8000/media/46/wallhaven-278479.jpg",
          "filename": "wallhaven-278479.jpg",
          "post": 46
        },
        {
          "id": 17,
          "file": "http://localhost:8000/media/46/tg_image_1211843334.jpeg",
          "filename": "tg_image_1211843334.jpeg",
          "post": 46
        }
      ],
      "links": [
        {
          "id": 14,
          "link": "https://inforeactor.ru/172142-stala-izvestna-cena-novoi-besprovodnoi-zaryadki-apple-airpower",
          "title": "Стала известна цена новой беспроводной зарядки Apple AirPower",
          "desc": "Беспроводная зарядка Apple AirPower станет доступна для покупки через год после анонса. Об этом пишет iXBT.com.",
          "image": "https://static.inforeactor.ru/uploads/2018/08/15/orig-1534303562f0839adcc1db248357e6a7aead95f913.jpeg",
          "post": 46
        },
        {
          "id": 15,
          "link": "yandex.ru",
          "title": "Яндекс",
          "desc": "Найдётся всё",
          "image": "https://yastatic.net/morda-logo/i/share-logo-ru.png",
          "post": 46
        }
      ],
      "created_at": "2018-08-15T05:20:38.770056Z",
      "text": "Аналитик компании Trend Force назвал предположительные цены трех новых iPhone от компании Apple. По мнению эксперта, обновленный iPhone X будет стоить дешевле предшественника, а самым дорогим смартфоном станет новый iPhone X Plus."
    }
  ]
}
```

**POST /api/posts/**
Создание поста
Параметры:
* text - string (required)
* media_files - array of files
* links - array of strings

```
ALLOWED_MEDIA_FORMATS = ['png', 'jpeg', 'jpg', 'bmp',
                         'mov', 'mpeg4', 'mp4', 'avi', 'wmv']
```
**Response Example**
```
{
    "id": 53,
    "user": {
        "id": 3,
        "username": "soapyhead",
        "email": "rta@tigrio.ru"
    },
    "likes_count": 0,
    "likes": [],
    "media_files": [
        {
            "id": 20,
            "file": "/media/53/tg_image_1211843334.jpeg",
            "filename": "tg_image_1211843334.jpeg",
            "post": 53
        }
    ],
    "links": [
        {
            "id": 18,
            "link": "yandex.ru",
            "title": "Яндекс",
            "desc": "Найдётся всё",
            "image": "https://yastatic.net/morda-logo/i/share-logo-ru.png",
            "post": 53
        }
    ],
    "created_at": "2018-08-15T07:30:14.566072Z",
    "text": "Hello World"
}
```

**GET /api/posts/{id}/**
Получить конкретный пост

**PUT /api/posts/{id}/ or PATCH /api/posts/{id}/**
Изменить пост (доступно только автору поста)
**Request Example**:
```
{
	"text": "Updated post text",
	"links": ["https://inforeactor.ru/172142-stala-izvestna-cena-novoi-besprovodnoi-zaryadki-apple-airpower", "yandex.ru"]
}
```

**DELETE /api/posts/{id}/**
Удаление поста (доступно только автору поста)

**POST /api/posts/{id}/like/**
Лайк пост. Юзер может лайкнуть пост только 1 раз, повторный лайк деактивирует лайк. Третий запрос активирует лайк, соответственно, и тд.