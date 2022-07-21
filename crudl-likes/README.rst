=============================
crudl-likes
=============================

.. image:: https://badge.fury.io/py/crudl-likes.svg
    :target: https://badge.fury.io/py/crudl-likes

.. image:: https://travis-ci.org/triplee12/crudl-likes.svg?branch=master
    :target: https://travis-ci.org/triplee12/crudl-likes

.. image:: https://codecov.io/gh/triplee12/crudl-likes/branch/master/graph/badge.svg
    :target: https://codecov.io/gh/triplee12/crudl-likes

Django crudl app for liking anything on your website.

Documentation
-------------

The full documentation is at https://crudl-likes.readthedocs.io.

Quickstart
----------

Install crudl-likes::

    pip install crudl-likes

Add it to your `INSTALLED_APPS`:

.. code-block:: python

    INSTALLED_APPS = (
        ...
        'likes.apps.LikesConfig',
        ...
    )

Add crudl-likes's URL patterns:

.. code-block:: python

    from likes import urls as likes_urls


    urlpatterns = [
        ...
        url(r'^', include(likes_urls)),
        ...
    ]

Features
--------

* TODO

Running Tests
-------------

Does the code actually work?

::

    source <YOURVIRTUALENV>/bin/activate
    (myenv) $ pip install tox
    (myenv) $ tox


Development commands
---------------------

::

    pip install -r requirements_dev.txt
    invoke -l


Credits
-------

Tools used in rendering this package:

*  Cookiecutter_
*  `cookiecutter-djangopackage`_

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`cookiecutter-djangopackage`: https://github.com/pydanny/cookiecutter-djangopackage
