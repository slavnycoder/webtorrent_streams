# Generated by Django 2.2.6 on 2019-10-14 18:35

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0005_auto_20191014_1726'),
    ]

    operations = [
        migrations.RenameField(
            model_name='user',
            old_name='following',
            new_name='followed',
        ),
    ]
