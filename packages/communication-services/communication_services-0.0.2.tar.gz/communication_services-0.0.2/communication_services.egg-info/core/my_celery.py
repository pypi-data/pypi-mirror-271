from __future__ import absolute_import, unicode_literals
import os
from core.my_celery import Celery

# Set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.my_settings')

app = Celery('core')

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
app.config_from_object('django.conf:settings', namespace='CELERY')

# ------------------------------------------------------------
# Set the broker URL programmatically
# ------------------------------------------------------------
# app.conf.update(
#     broker_url='amqp://notify_broker:notify_broker@localhost'
# )
# ------------------------------------------------------------
# Update broker transport options to include credentials
# app.conf.broker_transport_options = {
#     'host': 'localhost',
#     'port': 15672,
#     'username': 'notify_broker',
#     'password': 'notify_broker',
#     'virtual_host': '/',
#     'ssl': False,  # Set to True if using SSL/TLS
# }
# ------------------------------------------------------------
# app.conf.broker_url = 'amqp://your_username:your_password@localhost:5672//'
# ------------------------------------------------------------


# Load task modules from all registered Django app configs.
app.autodiscover_tasks()