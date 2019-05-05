Software stack
==============

fooskill has three main components: its database, its backend server
(which serves a `REST API`_), and its frontend server (which consumes
the REST API).

The database is managed by `PostgreSQL`_, but is largely handled through
an `ORM`_ in the backend server.

The backend server uses the `Django`_ web framework and the `Django REST
Framework`_ to serve its API for the frontend.

The frontend is written in `React`_ and uses lots of UI components from
`React Bootstrap`_.


.. _Django: https://www.djangoproject.com/
.. _Django REST Framework: https://www.django-rest-framework.org/
.. _ORM : https://en.wikipedia.org/wiki/Object-relational_mapping
.. _PostgreSQL: https://www.postgresql.org/
.. _React: https://reactjs.org/
.. _React Bootstrap: https://react-bootstrap.github.io/
.. _REST API: https://en.wikipedia.org/wiki/Representational_state_transfer
