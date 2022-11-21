# Generated by Django 4.1.2 on 2022-11-21 19:45

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_userlogin'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userlogin',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='logins', to=settings.AUTH_USER_MODEL),
        ),
    ]
