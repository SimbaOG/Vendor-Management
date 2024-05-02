# Generated by Django 4.2.2 on 2024-05-02 11:07

from django.db import migrations, models

import accounts.auth.helpers


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='tokenmanager',
            name='valid_upto',
            field=models.DateTimeField(default=accounts.auth.helpers.valid_upto_date),
        ),
    ]