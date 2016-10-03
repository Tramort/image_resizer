============
ImageResizer
============

It's solution of test task.
In brief, need to create service to decrease image by two times by using python, some libs and some technologies.

This app have rest api and support websocket connections.
For rest api docs used drfdocs generator (to see need to install and visit http://localhost:8000/docs).

Used libs: django, celery, channels, django rest framework and other.


Installation
------------
Use python 2.7 or python 3.4+

.. code::

  git clone https://github.com/Tramort/image_resizer.git
  cd image_resizer
  pip install -r requirements.txt
  python manage.py check
  python manage.py makemigrations
  python manage.py migrate
  python manage.py test

Usage
------------
.. code::

  python manage.py celery worker
  
and  
  
.. code::

  python manage.py runserser

