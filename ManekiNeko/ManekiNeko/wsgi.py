"""
WSGI config for ManekiNeko project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.9/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

from bot.model.response import ResponseModelFitting

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "ManekiNeko.settings")

application = get_wsgi_application()

# training model
res_model = ResponseModelFitting()
res_model.start()
