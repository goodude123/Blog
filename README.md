# Blog

Application that allows users to share their thoughts, stories or asking question. Everything what can be shared between people.

[Page Link](http://blogapp-mm.herokuapp.com/)

### Features
- login and register user system
- adding posts visible for logged users
- deleting views by owners or administator
- REST Api for mobile application

### Future improves
- add sections to group posts, articles
- add permissions and groups to allow people share some
  posts personally

### Technologies:
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
