from django import forms
from django.contrib.auth.forms import UserCreationForm

from .models import Owner, Trainer, User, places, gender
from cloudinary.forms import CloudinaryFileField

# Create your forms here.
class OwnerForm(UserCreationForm):
    location = forms.ChoiceField(choices=places)
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput, required=True)
    password2 = forms.CharField(label='Password Confirm', widget=forms.PasswordInput, required=True)
    class Meta:
        model = User
        fields =('username','first_name','last_name','email','phone','location')
        extra_kwargs = {'password1':{'write_only':True,'min_length':6}}

    def create(self,validated_data):
        return User.objects.create_user(**validated_data)
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.is_owner = True
        if commit:
            user.save()
        owner = Owner.objects.get(user=user)
        owner.location= self.cleaned_data.get('location')
        owner.save()
        return user
   
class TrainerForm(UserCreationForm):
    location = forms.ChoiceField(choices=places)
    gender = forms.ChoiceField(choices=gender)
    image= CloudinaryFileField()
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput, required=True)
    password2 = forms.CharField(label='Password Confirm', widget=forms.PasswordInput, required=True)
    class Meta:
        model = User
        fields =('username','first_name','last_name','email','gender','phone','image','location')
        extra_kwargs = {'password1':{'write_only':True,'min_length':6}}

    def create(self,validated_data):
        return User.objects.create_user(**validated_data)
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.is_trainer = True
        if commit:
            user.save()
        trainer = Trainer.objects.get(user=user)
        trainer.location= self.cleaned_data.get('location')
        trainer.image= self.cleaned_data.get('image')
        trainer.save()
        return user
    
        
class LoginForm(forms.Form):
    username = forms.CharField()
    password=forms.CharField(max_length=20, widget=forms.PasswordInput)
   