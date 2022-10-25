from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.db import transaction

from .models import User
    
class OwnerForm(UserCreationForm):
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput, required=True)
    password2 = forms.CharField(label='Password Confirm', widget=forms.PasswordInput, required=True)
    class Meta:
        model = User
        fields =('username','email','phone')
        extra_kwargs = {'password1':{'write_only':True,'min_length':6}}

    def create(self,validated_data):
        return User.objects.create_user(**validated_data)
    
    @transaction.atomic
    def save(self):
        user = super().save(commit=False)
        user.is_Owner = True
        user.save()
        return user
    
class TrainerForm(UserCreationForm):
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput, required=True)
    password2 = forms.CharField(label='Password Confirm', widget=forms.PasswordInput, required=True)
    class Meta:
        model = User
        fields =('username','email','phone')
        extra_kwargs = {'password1':{'write_only':True,'min_length':6}}

    def create(self,validated_data):
        return User.objects.create_user(**validated_data)
    
    @transaction.atomic
    def save(self):
        user = super().save(commit=False)
        user.is_Trainer = True
        user.save()
        return user