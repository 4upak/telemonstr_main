# Generated by Django 4.0.1 on 2022-04-02 13:12

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('proxy', '0001_initial'),
        ('accounts', '0020_remove_funnel_message_funnel_delete_funnel_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='telegram_account',
            name='proxy',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='proxy.proxy'),
        ),
        migrations.DeleteModel(
            name='Proxy',
        ),
    ]
