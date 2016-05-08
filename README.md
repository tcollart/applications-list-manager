# Simple App
------------
A simple app to manage a list of applications.

An application has a description, a zip file which can be accessed by an url, and can be public or private.

Three pages are available :
- a page listing all the public applications and the current logged in user private ones
- a page to edit your application
- a page to upload a new application

Project made using `Python 3.5`, `django 1.8` and `bootstrap3`.

```
$ pip install -r requirements.txt
$ python manage.py migrate
$ python manage.py runserver
```
