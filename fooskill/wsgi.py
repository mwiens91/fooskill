"""
WSGI config for fooskill project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/2.1/howto/deployment/wsgi/
"""

import os
import warnings
from django.core.wsgi import get_wsgi_application
import dotenv


# Load environment variables from .env file
with warnings.catch_warnings():
    warnings.filterwarnings("error")

    try:
        dotenv.read_dotenv(
            os.path.join(os.path.dirname(os.path.dirname(__file__)), ".env")
        )
    except UserWarning:
        raise FileNotFoundError("Could not find .env!")

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "fooskill.settings")

application = get_wsgi_application()
