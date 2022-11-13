from django import forms

from mainapp.models import Booking, BusinessHours, Dog, Post, Review
from accounts.choices import HOUR_CHOICES, DAYS_OF_WEEK
from datetime import datetime
from accounts.utilities import check_free_time
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

class HoursForm(forms.ModelForm):
    day= forms.ChoiceField(choices=DAYS_OF_WEEK)
    start= forms.ChoiceField(choices=HOUR_CHOICES)
    end= forms.ChoiceField(choices=HOUR_CHOICES)
    class Meta:
        model= BusinessHours
        fields=['day', 'start','end','open_closed']
        
class BookingForm(forms.ModelForm):

    def __init__(self,*args,**kwargs):
        super(BookingForm,self).__init__(*args,**kwargs)
        self.fields['book_date'].label = "book Date"
        self.fields['book_time'].label = "book Time"

    def clean(self):
        cleaned_data = super(BookingForm,self).clean()
        booking_number = f"{cleaned_data.get('book_date'):%Y%m%d}{cleaned_data.get('book_time'):%H%M}"
        if Booking.objects.filter(booking_number=booking_number).exists():
            today = datetime.today()
            d = today.day
            m = today.month
            y = today.year
            
            today_bookings = Booking.objects.filter(book_date__year=y,book_date__month=m, book_date__day=d)

            today_time_slot = today_bookings.values('book_date')
            today_time_slot_list = [h['book_date'] for h in list(today_time_slot)]
            
            all_time_slot = [7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18]

            available_slot = check_free_time(all_time_slot, today_time_slot_list)
            if available_slot:
                message = f"Requested slot is already booked, please choose another time in {available_slot}."
                raise forms.ValidationError(message)
            else:
                message = "The are not available slot for this booking today."
                raise forms.ValidationError(message)
        
    
    class Meta:
        model = Booking
        fields = ('book_date','book_time')
        widgets = {
            'book_date': forms.DateInput(attrs={'type': 'date'}),
            'book_time':forms.Select(choices=HOUR_CHOICES)
        }