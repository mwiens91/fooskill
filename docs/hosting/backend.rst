Hosting the backend server
==========================

.. highlight:: console

Cloning the fooskill repository
-------------------------------

The first thing you need to do is clone the fooskill repository. With
HTTPS, do this with ::

    $ git clone https://github.com/mwiens91/fooskill.git

Or with SSH, do it with ::

    $ git clone git@github.com:mwiens91/fooskill.git

or clone your `fork <https://help.github.com/en/articles/fork-a-repo>`_.

Setting up a virtual environment
--------------------------------

Next you need to set up fooskill's environment. First, enter the
repository's backend directory::

    $ cd fooskill/backend

Create and activate a new Python 3.x [#pythonversions]_ virtual
environment using your preferred method [#virtualenvwrapper_note]_ , or
with ::

    $ python3 -m venv venv
    $ source venv/bin/activate

After you've activated a virtual environment, you need to install
fooskill's requirements::

    $ pip install -r requirements.txt


Setting up environment variables
--------------------------------

fooskill collects variables unique to your locale from a ``.env`` file
at the base of the backend directory at runtime.

To create your ``.env`` file, copy the included example ``.env.example``
file to ``.env``::

    $ cp .env.example .env

Make sure that ``DEBUG`` is set to ``True``. We'll modify the
``DATABASE_*`` variables in the next section.

Setting up a PostgreSQL database
--------------------------------

The next step is to set up a PostgreSQL database for the project; for
simplicity, this documentation assumes you are using a Debian-like
operating system (e.g., Ubuntu). [#postgres_reference]_ First, make sure
you have the necessary packages; on Ubuntu, these packages can be
installed with ::

    $ sudo apt install python3-dev libpq-dev postgresql postgresql-contrib

The next step is to launch a Postgres session as the ``postgres`` user::

    $ sudo -u postgres psql

You should see a prompt like the following::

    psql (11.2 (Ubuntu 11.2-1))
    Type "help" for help.

    postgres=#

Now, having a username ``username``, and password ``password`` in mind,
enter the following commands: [#postgres_commands]_

.. code-block:: none

    postgres=# CREATE DATABASE fooskill;
    postgres=# CREATE USER username WITH PASSWORD 'password';
    postgres=# ALTER ROLE username SET client_encoding TO 'utf8';
    postgres=# ALTER ROLE username SET default_transaction_isolation TO 'read committed';
    postgres=# ALTER ROLE username SET timezone TO 'UTC';
    postgres=# GRANT ALL PRIVILEGES ON DATABASE fooskill TO username;
    postgres=# \q

Once that's done fill in the corresponding variables (``DATABASE_NAME``,
``DATABASE_USER``, and ``DATABASE_USER_PASSWORD``) in your ``.env``.

Now that the database is set up, migrate fooskill's database schema
with::

    $ ./manage.py migrate

Creating an admin user
----------------------

Create an admin user by running the following::

    $ ./manage.py createsuperuser

You should be prompted for your username, email, and password::

    Username (leave blank to use 'matt'):
    Email address: matt@email.com
    Password:
    Password (again):
    Superuser created successfully.

Note that the Django admin user credentials provided above are
completely independent of the PostgreSQL user credentials we set up for
the database.

Running the server
------------------

Now all you should need to do is ::

    $ ./manage.py runserver

and point your browser to ``127.0.0.1:8000``!

.. Footnotes
.. [#pythonversions] fooskill officially supports Python ≥ 3.6, but
   earlier versions of Python 3 will likely work just fine.
.. [#virtualenvwrapper_note] As an alternative to the virtual
   environment creation method shown, I highly recommend using
   `virtualenvwrapper
   <https://virtualenvwrapper.readthedocs.io/en/latest/>`_ to create and
   manage your Python virtual environments.
.. [#postgres_reference] The instructions for setting up PostgreSQL are
    adapted from Digital Ocean's guide `here
    <https://www.digitalocean.com/community/tutorials/how-to-use-postgresql-with-your-django-application-on-ubuntu-16-04>`_.
.. [#postgres_commands] See `Django's docs
   <https://docs.djangoproject.com/en/dev/ref/databases/#optimizing-postgresql-s-configuration>`_
   for why the commands shown are used.
