# Приложение Quiz

[Ссылка на общее описание тестовое задания](https://yadi.sk/i/F4eBBIin1a4AZA)

## Почта для вопросов и результатов выполнения тестового
[internship.web@simbirsoft.com](internship.web@simbirsoft.com)

## Общий функционал
Приложение, которое позволяет пользователю пройти тестирование по вопросам с
заданными вариантами ответа, проверяет ответы и показывает пользователю результат.
Ответ на вопрос считается правильным, если пользователь выбрал все правильные варианты ответа. Если пользователь выбрал не все правильные варианты, либо лишние варианты - вопрос считается неправильным.

## Основные технологии
* Python
* Django
* Docker Compose

### Комментарии по выполнению ТЗ
#### Структура приложения ####
___
core app 

DJANGO DRF 

* GET api/quizzes/ - список викторин 
* GET api/quizzes/started - список незаконченных викторин
* GET api/quizzes/started - список начатых викторин
* POST api/quizzes/started - начать викторину
```
{"uuid":"1"}
```
* GET api/quizzes/finished - список законченных викторин
* GET api/quizzes/<slug>/question - получить вопрос
* POST api/quizzes/<slug>/question - отправить ответ
```
{"question_uuid":"2-1","choices":["2-1-3"]}
```
* GET api/quizzes/<slug>/question/prev - получить предыдущий вопрос
* PATCH api/quizzes/<slug>/question/prev - обновить ответ на предыдущий вопрос
```
{"question_uuid":"2-1","choices":["2-1-2"]}
```
* GET api/quizzes/<slug>/score - получить количество очков

___
#### front app ####

alpine js, bootstrap 5

Django session based authentication,

Django user management

user: test_user, password: 123 

* "" - список викторин
* /quizz/<slug> - викторина

#### tests ####
```

pytest tests/test_api.py
pytest tests/test_core.py
```

#### fixture folder ####
/fixture 