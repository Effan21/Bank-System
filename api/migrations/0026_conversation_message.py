# Generated by Django 4.2.1 on 2023-06-18 23:00

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0025_faq'),
    ]

    operations = [
        migrations.CreateModel(
            name='Conversation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('admin', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.agent')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='conversations', to='api.client')),
            ],
        ),
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.IntegerField(choices=[(0, 'User'), (1, 'Admin')])),
                ('content', models.TextField()),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('conversation', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='messages', to='api.conversation')),
            ],
            options={
                'ordering': ['timestamp'],
            },
        ),
    ]
