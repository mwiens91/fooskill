.. _contributing:

Contributing
============

.. highlight:: console

Contributions to fooskill are welcome! However, before submitting a pull
request, please ensure that your code style is consistent with what is
already in fooskill!

Backend code style
------------------

fooskill's backend code follows `Google's Python Style Guide`_ and
`Django's Coding Style Guide`_ closely. While you don't need to
intimately know both of these style guides before contributing, if you
contribute something doesn't follow them, you'll likely be asked to
change your contribution so that it does.

For code formatting, life is a lot simpler. fooskill's backend uses
`Black`_ to format all of its code. All you need to do, after installing
Black, is to run ::

   $ black .

at the root of the backend directory and your code will be formatted
automatically.

Frontend code style
-------------------

fooskill's frontend code uses `Prettier`_ to format all of its code.
After installing Prettier, simply run ::

   $ prettier --write modifiedFile.js

on any files you modify.

Database backups
----------------

To get started with fooskill development, it's useful to have some data
to work with. Until there's some stock data available for everyone to
use, I'll likely be happy to provide a database backup you can use to
develop with—just contact me personally for this.

.. _Black: https://docs.djangoproject.com/en/dev/internals/contributing/writing-code/coding-style/
.. _Django's Coding Style Guide: https://docs.djangoproject.com/en/dev/internals/contributing/writing-code/coding-style/
.. _Google's Python Style Guide: https://github.com/google/styleguide/blob/gh-pages/pyguide.md
.. _Prettier: https://github.com/prettier/prettier
