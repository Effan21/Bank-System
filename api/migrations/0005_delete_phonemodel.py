# Generated by Django 4.2.1 on 2023-06-07 10:37

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0004_phonemodel'),
    ]

    operations = [
        migrations.DeleteModel(
            name='phoneModel',
        ),
    ]