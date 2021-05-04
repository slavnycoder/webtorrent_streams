# Generated by Django 2.2.9 on 2020-03-11 15:39

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('streams', '0009_auto_20200302_2313'),
    ]

    operations = [
        migrations.AddField(
            model_name='stream',
            name='dttm_last_chunk',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AddField(
            model_name='stream',
            name='is_started',
            field=models.BooleanField(default=False),
        ),
    ]