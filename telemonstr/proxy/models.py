from django.db import models

class Proxy(models.Model):

    type = models.CharField(max_length = 20)
    host = models.GenericIPAddressField(unique=True)
    port = models.CharField(max_length = 20)
    login = models.CharField(max_length = 100)
    password = models.CharField(max_length = 255)