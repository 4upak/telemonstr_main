# Generated by Django 4.0.1 on 2022-02-07 11:45

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0008_telegram_account_str_password'),
    ]

    operations = [
        migrations.RenameField(
            model_name='telegram_account',
            old_name='str_password',
            new_name='twoFA_password',
        ),
        migrations.RemoveField(
            model_name='telegram_account',
            name='password',
        ),
    ]
