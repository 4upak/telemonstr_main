# Generated by Django 4.0.1 on 2022-02-07 11:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0009_rename_str_password_telegram_account_twofa_password_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='telegram_account',
            name='session_file',
            field=models.CharField(max_length=100, unique=True),
        ),
    ]
