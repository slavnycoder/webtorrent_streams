# Generated by Django 2.2.6 on 2019-10-27 22:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0013_chatban'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='userpic_filename',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
