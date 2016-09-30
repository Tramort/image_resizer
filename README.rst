============
ImageResizer
============

It's solution of test task.
In brief, need to create service to decrease image by two times by using python, some libs and some technologies.

For rest api docs used drfdocs generator (to see need to install and visit http://localhost:8000/docs).

Installation
------------
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

