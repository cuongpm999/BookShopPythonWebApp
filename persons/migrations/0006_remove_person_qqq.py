# Generated by Django 4.0.3 on 2022-03-29 02:33

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('persons', '0005_person_qqq'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='person',
            name='qqq',
        ),
    ]
