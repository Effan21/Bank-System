# Generated by Django 4.2.1 on 2023-06-02 00:49

from django.db import migrations, models
import django_cryptography.fields


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='carte_credit',
            name='cvv',
            field=django_cryptography.fields.encrypt(models.IntegerField(max_length=3)),
        ),
    ]