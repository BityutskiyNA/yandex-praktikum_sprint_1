# Generated by Django 3.2 on 2022-10-03 14:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('movies', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='personfilmwork',
            name='created',
            field=models.DateField(auto_now_add=True),
        ),
    ]