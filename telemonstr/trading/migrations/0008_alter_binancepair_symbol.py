# Generated by Django 4.0.1 on 2022-06-10 13:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('trading', '0007_alter_binancepair_base_asset_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='binancepair',
            name='symbol',
            field=models.CharField(max_length=20, unique=True),
        ),
    ]
