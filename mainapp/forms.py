from django import forms

from mainapp.models import Booking, BusinessHours, Clinic, Dog, Post, Review
# Create your forms here.
class DogForm(forms.ModelForm):
    class Meta:
        model= Dog
        fields=['dog_name', 'dog_age','dog_pic','dog_sex']

class PostForm(forms.ModelForm):
    class Meta:
        model= Post
        fields=['video_title', 'video_caption','video']

class ReviewForm(forms.ModelForm):
    class Meta:
        model= Review
        fields=['title', 'description']

class ClinicForm(forms.ModelForm):
    class Meta:
        model= Clinic
        fields=['clinic_name', 'clinic_location']

class HoursForm(forms.ModelForm):
    class Meta:
        model= BusinessHours
        fields=['day', 'start','end','open_closed']
        widgets = {
            'start': forms.TimeInput(attrs={'type': 'time'}),
            'end': forms.TimeInput(attrs={'type': 'time'})
        }
        
class BookForm(forms.ModelForm):
    class Meta:
        model= Booking
        fields=['email','date', 'time']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
            'time': forms.TimeInput(attrs={'type': 'time'})
        }