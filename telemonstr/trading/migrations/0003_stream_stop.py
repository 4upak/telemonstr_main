# Generated by Django 4.0.1 on 2022-06-09 09:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('trading', '0002_stream'),
    ]

    operations = [
        migrations.AddField(
            model_name='stream',
            name='stop',
            field=models.IntegerField(default=0),
        ),
    ]
