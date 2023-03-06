# Edutest
## _Technical Challenge Monet_

[![Django](https://cdn.iconscout.com/icon/free/png-256/django-12-1175186.png?f=avif&w=128)](https://docs.djangoproject.com/en/4.1/)

Prueba tecnica Monet
Python-django-REST.
- Exam management
- Singup Students

## Features

- Create User Student
- Create SuperUser
- Create Answer´s bank 
- Create Exams
- Endpoit For Student Present Test (Protected with JWT)

> The main objective of the Edutest design is to create a scalable and testable Django application built using SOLID principles. As part of the test, the adminUser needs to be modified to create a Student of type Admin django. Although Django's documentation suggests not doing this and instead creating a model with a one-to-one relationship, the test requirement has been taken into account. An endpoint has been created for student registration and login, with another endpoint for taking tests protected with JWT. Due to the previous modification, the student will only be able to access the admin and view their own answers, which are interpreted as the answers submitted for the test.


## Tech

Edutest use a open source project to work properly:

- [Python] - "there should be one—and preferably only one—obvious way to do it"

## Installation

Edutest requires :
>[python](https://www.python.org/) 
>[Django](https://www.djangoproject.com/)
>[djangorestframework](https://www.django-rest-framework.org/)
>[djangorestframework_simplejwt](https://pypi.org/project/djangorestframework-simplejwt/)

Install the dependencies and devDependencies and start the server.

```sh
pip install requirements.txt
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```


## Plugins

Edutest is currently extended with the following plugins.
Instructions on how to use them in your own application are linked below.

| Plugin | README |
| ------ | ------ |
| djangorestframework | [https://www.django-rest-framework.org/tutorial/quickstart/] |
| djangorestframeworkJWT | [https://django-rest-framework-simplejwt.readthedocs.io/en/latest/] |

## Requeriments:

Requerimientos de Aplicación Django
1. Crear modelos de Student, Test, Question, Answer ok
2. Endpoint para identificar a un estudiante y devolver su respectivo JWT
3. Endpoint protegido para registrar las respuestas de un estudiante
4. Modificaciones al Django Admin para que un estudiante pueda ingresar al portal y solo
ver sus propias respuestas a los tests

## Directory structure
~~~
edutest/
├── edutest/
│   ├── __init__.py
│   ├── asgi.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── testapp/
│   ├── migrations/
│   │   └── __init__.py
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── forms.py
│   ├── models.py
│   ├── serializers.py
│   ├── tests.py
│   ├── urls.py
│   └── views.py
├── .gitignore
├── manage.py
├── static
│   ├── __init__.py
│   └──  DER_Edutest.png
└── README.md
~~~
## Diagram Entity Relation

![Diagram Entity Relation](/static/DER_Edutest.png)



## End Points
##### admin
```sh
http://localhost:8000/admin/
```

##### Signup Student:

* POST  http://localhost:8000/student/signup/
    >Body (json)

    ~~~
    {
        "email": "correo@gmail.com",
        "first_name": "nombre",
        "last_name": "apellido",
        "password": "contraseña"
    }
    ~~~
    >cURL
    
        curl --location 'http://localhost:8000/student/signup/' \
        --data-raw '{
        "email": "correo@gmail.com",
        "first_name": "nombre",
        "last_name": "apellido",
        "password": "contraseña"
        }'

##### Api Token
* POST  http://localhost:8000/api/token/
    >Body (json)

    ~~~
    {"email": "email@mail.com", "password": "contraseña"}
    ~~~
    >cURL
    
        curl --location 'http://localhost:8000/api/token/' \
        --header 'Content-Type: application/json' \
        --data-raw '{"email": "correo@gmail.com", "password": "contraseña"}'
        
    
##### Student Answer
* POST  http://localhost:8000/student/answers/
    >body(json)

        | Request Heders |  | 
        | ------ | ------ |
        | Authorization | Bearer {{token}} |
        | Content-Type | application/json |
        
    ~~~
        {"test_id":1, "question": 1, "answers": "answer"}
    ~~~  
    >cURL
          
            curl --location 'http://localhost:8000/student/answers/' \
            --header 'Authorization: Bearer {{token}}' \
            --header 'Content-Type: application/json' \
            --data '{"test_id":1,"question": 1, "answers": "respuesta alumno logeado"}'
            
            

    ```sh
    127.0.0.1:8000
    ```

## License

MIT

**Free Software!**
**JaimeCabrera.**
[//]: # 

   [Python]: <https://docs.python.org/3/>
