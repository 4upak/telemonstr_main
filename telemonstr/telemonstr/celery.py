import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'telemonstr.settings')

app = Celery('telemonstr')
app.config_from_object('django.conf:settings', namespace='CELERY')
print(app)
app.autodiscover_tasks()