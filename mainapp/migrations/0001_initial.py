# Generated by Django 4.1.2 on 2022-11-14 18:21

import cloudinary.models
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Service',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('services', models.CharField(choices=[('obedience', 'Obedience-Training'), ('trick', 'Trick_Skill_Training'), ('behavior', 'Behavior Modification'), ('puppy', 'Puppy Training'), ('security', 'Security Program'), ('anxiety', 'Separation Anxiety')], max_length=50)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='service', to='accounts.trainer')),
            ],
        ),
        migrations.CreateModel(
            name='Review',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('description', models.TextField()),
                ('reviewed', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reviewed', to='accounts.trainer')),
                ('reviewer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reviewer', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('video_title', models.CharField(max_length=100)),
                ('video_caption', models.TextField()),
                ('video', cloudinary.models.CloudinaryField(blank=True, max_length=255)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='posts', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Hours',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('day', models.CharField(choices=[('Monday', 'Monday'), ('Tuesday', 'Tuesday'), ('Wednesday', 'Wednesday'), ('Thursday', 'Thursday'), ('Friday', 'Friday'), ('Saturday', 'Saturday'), ('Sunday', 'Sunday')], max_length=10, unique=True)),
                ('start', models.TimeField(null=True)),
                ('end', models.TimeField(null=True)),
                ('open_closed', models.BooleanField(default=False)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='business_hours', to='accounts.trainer')),
            ],
        ),
        migrations.CreateModel(
            name='Dog',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('dog_name', models.CharField(max_length=50)),
                ('dog_age', models.IntegerField()),
                ('dog_pic', cloudinary.models.CloudinaryField(max_length=255, verbose_name='image')),
                ('dog_sex', models.CharField(choices=[('male', 'Male'), ('female', 'Female')], max_length=10)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='dog', to='accounts.owner')),
            ],
        ),
        migrations.CreateModel(
            name='Clinic',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('clinic_name', models.CharField(max_length=50, unique=True)),
                ('clinic_location', models.CharField(choices=[('Nairobi-CBD', 'Nairobi-CBD'), ('Nairobi-Ngong Road', 'Nairobi-Ngong Road'), ('Nairobi-Thika Road', 'Nairobi-Thika Road'), ('Nairobi-Waiyaki Way', 'Nairobi-Waiyaki Way'), ('Nairobi-Outering Road', 'Nairobi-Outering Road'), ('Nairobi-Jogoo Road', 'Nairobi-Jogoo Road'), ('Nairobi-Kiambu Road', 'Nairobi-Kiambu Road'), ('Nairobi-Westlands', 'Nairobi-Westlands'), ('Kiambu', 'Kiambu'), ('Kisii', 'Kisii'), ('Kikuyu', 'Kikuyu'), ('Nakuru', 'Nakuru'), ('Eldoret', 'Eldoret'), ('Kakamega', 'Kakamega'), ('Kisumu', 'Kisumu'), ('Mombasa', 'Mombasa')], max_length=50)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='clinic', to='accounts.trainer')),
            ],
        ),
        migrations.CreateModel(
            name='Booking',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('book_date', models.DateField(null=True)),
                ('book_time', models.TimeField(null=True)),
                ('booking_number', models.CharField(max_length=50, unique=True)),
                ('trainer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='book', to='accounts.trainer')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='bookings', to='accounts.owner')),
            ],
        ),
        migrations.AddConstraint(
            model_name='hours',
            constraint=models.CheckConstraint(check=models.Q(('start__lte', models.F('end'))), name='start_before_end'),
        ),
    ]
