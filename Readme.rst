**************************************
Buildout for Demo Watermarking project
**************************************

Questions and assumptions
=========================

*General assumptions:*
    * support only epub format, all other treats as unsupported
    * simple url validation
    * file size limitation 100 MB
    * not sure about way of result delivery

*Confusing things that I don't get:*
    * "A REST GET endpoint, you determine the URL."


Installation notes
==================

Pre-requirements
----------------

You need to have python 3.5 or newest to build this environment, also you need to have python2.7 for running acceptance tests.

Environment assembling
----------------------

For environment set up zc.buildout is used (https://pypi.python.org/pypi/zc.buildout/2.4.0)

Before building it you need to set up environment version you would like to have.
Currently there is *production* and *development* configuration available, to
set config do following:

.. code-block:: bash

    $ cp buildout.cfg.example buildout.cfg
    $ vim buildout.cfg

and in buildout.cfg uncomment one of profiles extends  you would like to be
activated, for example if you would like your environment to be build in
*production* mode the part section of buildout should look like this:

.. code-block::

    [buildout]
    extends =
        profiles/production.cfg
    #    profiles/devel.cfg


To build buildout run following command:

.. code:: bash

    $ python3 bootstrap-buildout.py
    $ bin/buildout

And do not forget to syncdb:

.. code-block:: bash

    $ bin/django syncdb

Frontend part of application is located in ngbp folder. It requeires to have
installed Node.js on system. Frontend are based on https://github.com/ngbp/ngbp


Project structure
=================

This project has two independent parts:
    * front-end
    * back-end

Front end
---------

Front-end doesn't care about back-end at all and can be used separately,
it's single file javascript application based on AngularJS and ngpb
template.

TODO: describe API calls here

Back end
--------

Back-end is based on Django and django-rest-framework and provides API for
front-end app cals.

TODO: describe API calls here


Running application
===================

To start djnago server run command

.. code:: bash

    bin/django runserver

or use gunicorn as wsgi server:

.. code:: bash

    env DJANGO_SETTINGS_MODULE=watermarking_web_app.production bin/gunicorn watermarking_web_app.wsgi

If you want to play around frontend then read ngbp instruction. In most cases
if would be enough to have buildout built in development and run following
commands:

.. code-block:: bash

    $ cd ngbp
    $ ../bin/grunt watch

After it you can edit front-end sources which is located in *ngbp/build/src*
folder.
