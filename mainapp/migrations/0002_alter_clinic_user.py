# Generated by Django 4.1.2 on 2022-11-13 07:38

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
        ('mainapp', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='clinic',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='clinic', to='accounts.trainer'),
        ),
    ]
