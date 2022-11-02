# Generated by Django 4.1.2 on 2022-11-02 13:36

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
        ('mainapp', '0003_booking'),
    ]

    operations = [
        migrations.CreateModel(
            name='Book',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_date', models.DateTimeField(default=datetime.datetime(2022, 11, 2, 13, 36, 31, 732267, tzinfo=datetime.timezone.utc))),
                ('book_date', models.DateField(null=True)),
                ('book_time', models.TimeField(null=True)),
                ('booking_number', models.CharField(max_length=50, unique=True)),
                ('trainer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='boo', to='accounts.trainer')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='booking', to='accounts.owner')),
            ],
        ),
    ]