# Generated by Django 4.0.6 on 2022-07-25 14:30

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('network', '0003_connections_delete_follow'),
    ]

    operations = [
        migrations.AlterField(
            model_name='connections',
            name='followers',
            field=models.ManyToManyField(null=True, related_name='followers', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='connections',
            name='following',
            field=models.ManyToManyField(null=True, related_name='following', to=settings.AUTH_USER_MODEL),
        ),
    ]
