from django import forms

from mainapp.models import Dog, Post, Review

# Create your forms here.
class DogForm(forms.ModelForm):
    class Meta:
        model= Dog
        fields=['dog_name', 'dog_age','dog_pic','dog_sex']

class PostForm(forms.ModelForm):
    class Meta:
        model= Post
        fields=['title', 'description','video']

class ReviewForm(forms.ModelForm):
    class Meta:
        model= Review
        fields=['title', 'description']
