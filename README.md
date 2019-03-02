# Blog

Web blog application.

Application that allows users to share their industries.

## Features
* login/register user
* the ability to add posts for logged users
* REST Api for mobile application


## Technologies:
  - Python 3.6.7
  - Django 2.1.5
  - Django REST Framework 3.9.0
  - Django Filter
  - SQLAlchemy
  
## Launch
Clone repository
```
$ git clone https://github.com/michal-mietus/blog.git
```

Run migrations
```
$ python3 manage.py makemigrations
$ python3 manage.py migrate
```

Now you can start your application.
```
$ python3 manage.py runserver
```
