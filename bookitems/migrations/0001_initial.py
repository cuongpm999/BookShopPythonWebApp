# Generated by Django 4.0.3 on 2022-03-08 07:50

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('books', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='BookItem',
            fields=[
                ('barCode', models.CharField(max_length=255, primary_key=True, serialize=False)),
                ('price', models.FloatField()),
                ('discount', models.FloatField()),
                ('img', models.ImageField(upload_to='images/')),
                ('status', models.BooleanField(default=True)),
                ('book', models.OneToOneField(on_delete=django.db.models.deletion.RESTRICT, to='books.book')),
            ],
        ),
    ]