# Generated by Django 4.0.1 on 2022-06-09 09:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('trading', '0003_stream_stop'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bundle',
            name='date',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
