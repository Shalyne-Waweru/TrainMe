# Generated by Django 4.1.2 on 2022-11-13 07:32

import cloudinary.models
from django.conf import settings
import django.contrib.auth.models
import django.contrib.auth.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
                ('first_name', models.CharField(blank=True, max_length=150, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('email', models.EmailField(blank=True, max_length=254, verbose_name='email address')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('is_trainer', models.BooleanField(default=False, verbose_name='Dog_Trainer')),
                ('is_owner', models.BooleanField(default=False, verbose_name='Dog_Owner')),
                ('phone', models.CharField(max_length=10)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Trainer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', cloudinary.models.CloudinaryField(max_length=255, verbose_name='image')),
                ('bio', models.TextField()),
                ('gender', models.CharField(choices=[('male', 'Male'), ('female', 'Female')], max_length=10)),
                ('services', models.CharField(choices=[('obedience', 'Obedience-Training'), ('trick', 'Trick_Skill_Training'), ('behavior', 'Behavior Modification'), ('puppy', 'Puppy Training'), ('security', 'Security Program'), ('anxiety', 'Separation Anxiety')], max_length=255)),
                ('location', models.CharField(choices=[('Nairobi-CBD', 'Nairobi-CBD'), ('Nairobi-Ngong Road', 'Nairobi-Ngong Road'), ('Nairobi-Thika Road', 'Nairobi-Thika Road'), ('Nairobi-Waiyaki Way', 'Nairobi-Waiyaki Way'), ('Nairobi-Outering Road', 'Nairobi-Outering Road'), ('Nairobi-Jogoo Road', 'Nairobi-Jogoo Road'), ('Nairobi-Kiambu Road', 'Nairobi-Kiambu Road'), ('Nairobi-Westlands', 'Nairobi-Westlands'), ('Kiambu', 'Kiambu'), ('Kisii', 'Kisii'), ('Kikuyu', 'Kikuyu'), ('Nakuru', 'Nakuru'), ('Eldoret', 'Eldoret'), ('Kakamega', 'Kakamega'), ('Kisumu', 'Kisumu'), ('Mombasa', 'Mombasa')], max_length=40)),
                ('min_price', models.CharField(max_length=10)),
                ('max_price', models.CharField(max_length=10)),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='Dog_Trainer', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Owner',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('location', models.CharField(choices=[('Nairobi-CBD', 'Nairobi-CBD'), ('Nairobi-Ngong Road', 'Nairobi-Ngong Road'), ('Nairobi-Thika Road', 'Nairobi-Thika Road'), ('Nairobi-Waiyaki Way', 'Nairobi-Waiyaki Way'), ('Nairobi-Outering Road', 'Nairobi-Outering Road'), ('Nairobi-Jogoo Road', 'Nairobi-Jogoo Road'), ('Nairobi-Kiambu Road', 'Nairobi-Kiambu Road'), ('Nairobi-Westlands', 'Nairobi-Westlands'), ('Kiambu', 'Kiambu'), ('Kisii', 'Kisii'), ('Kikuyu', 'Kikuyu'), ('Nakuru', 'Nakuru'), ('Eldoret', 'Eldoret'), ('Kakamega', 'Kakamega'), ('Kisumu', 'Kisumu'), ('Mombasa', 'Mombasa')], max_length=40)),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='Dog_Owner', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
