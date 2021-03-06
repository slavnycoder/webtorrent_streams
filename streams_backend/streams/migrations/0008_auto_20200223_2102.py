# Generated by Django 2.2.9 on 2020-02-23 21:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('streams', '0007_chunk_prob'),
    ]

    operations = [
        migrations.AlterField(
            model_name='chunk',
            name='duration',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=4),
        ),
        migrations.AlterField(
            model_name='chunk',
            name='is_public',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='chunk',
            name='magnet_link',
            field=models.TextField(blank=True, null=True),
        ),
    ]
