from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0010_alter_client_contact'),
    ]

    operations = [
        migrations.RenameField(
            model_name='demandes_ouvertures_comptes',
            old_name='photo',
            new_name='user_pic',
        ),
        migrations.AddField(
            model_name='demandes_ouvertures_comptes',
            name='adresse',
            field=models.CharField(blank=True, max_length=100),
        ),
        migrations.AddField(
            model_name='demandes_ouvertures_comptes',
            name='code_secret',
            field=models.CharField(blank=True, max_length=100),
        ),
        migrations.AddField(
            model_name='demandes_ouvertures_comptes',
            name='date_naissance',
            field=models.DateField(),
        ),
        migrations.AddField(
            model_name='demandes_ouvertures_comptes',
            name='signature_pic',
            field=models.ImageField(blank=True, upload_to='signature'),
        ),
    ]
