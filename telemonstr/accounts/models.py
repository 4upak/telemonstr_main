from django.db import models

class Telegram_account(models.Model):

    telegram_user_id = models.BigIntegerField(blank=True, null=True)
    session_file = models.CharField(max_length = 100, unique=True)
    created_at = models.DateTimeField(auto_now_add = True)
    register_time = models.IntegerField(default = 0)
    proxy = models.GenericIPAddressField(protocol='IPv4', unpack_ipv4=False, null=True)
    first_name = models.CharField(max_length = 250, default='-', null=True)
    last_name = models.CharField(max_length = 250, default='-', null=True)
    last_check_time = models.DateTimeField(auto_now=False, auto_now_add=False, null=True)
    deleted = models.BooleanField(default=False)
    twoFA = models.BooleanField(default=False)
    twoFA_password = models.CharField(max_length = 250, blank=True)
    avatar = models.CharField(max_length = 250, default='-')
    username = models.CharField(max_length = 250, default='-', null=True)
    work = models.BooleanField(default=0)
    restricted = models.BooleanField(default=0)
    action =  models.CharField(max_length = 255, default='-')
    online = models.BooleanField(default=0)
    invite_restricted = models.BooleanField(default=0)
    message_restricted = models.BooleanField(default=0)

class Proxy(models.Model):

    type = models.CharField(max_length = 20)
    host = models.GenericIPAddressField(unique=True)
    port = models.CharField(max_length = 20)
    login = models.CharField(max_length = 100)
    password = models.CharField(max_length = 255)


