# Generated by Django 4.0.3 on 2022-03-29 02:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('persons', '0002_alter_address_number'),
    ]

    operations = [
        migrations.AddField(
            model_name='person',
            name='xx',
            field=models.IntegerField(default=0),
        ),
    ]