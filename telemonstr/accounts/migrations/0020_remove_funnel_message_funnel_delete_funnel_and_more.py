# Generated by Django 4.0.1 on 2022-04-02 12:54

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0019_alter_funnel_funnel_name'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='funnel_message',
            name='funnel',
        ),
        migrations.DeleteModel(
            name='Funnel',
        ),
        migrations.DeleteModel(
            name='Funnel_message',
        ),
    ]
