# Generated by Django 2.2.6 on 2019-10-20 17:28

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0012_auto_20191018_1956'),
    ]

    operations = [
        migrations.CreateModel(
            name='ChatBan',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('expires', models.DateTimeField()),
                ('streamer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='banned_users', to=settings.AUTH_USER_MODEL)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='bans', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'unique_together': {('streamer', 'user')},
            },
        ),
    ]
