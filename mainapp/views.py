from django.shortcuts import render, redirect, HttpResponse, HttpResponseRedirect
from django.views.generic import CreateView

from accounts.forms import *
from accounts.models import Owner, Trainer, User
# from accounts.choices import service

from django.contrib.auth import login,authenticate, logout
from django.urls import reverse_lazy
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from mainapp.forms import *
from mainapp.models import *

import requests
from .mpesa import MpesaAccessToken, LipanaMpesaPpassword

# Create your views here.
def index(request):
    trainers= Trainer.objects.all()
    return render(request, 'index.html',locals())

def appointments(request, id):
    trainer = Trainer.objects.get(id=id)
    appointments=Booking.filter_by_trainer(id=trainer.id)
    return render(request, 'appointments.html', locals())
    
@login_required(login_url='/accounts/login/owner')
def search(request):
    trainers= Trainer.objects.all()
    if 'location' in request.GET and request.GET["location"]:
        search_term = request.GET.get("location")
        searched_location = Trainer.search_by_location(search_term)
        message = f"{search_term}"

        return render(request, 'search.html',locals())

    else:
        message = "You haven't searched for any term"
    return render(request, 'search.html', locals())

class TrainerSignUpView(CreateView):
    model = User
    form_class = TrainerForm
    template_name = 'auth/trainer_reg.html'
    success_url =reverse_lazy('trainer_login')

    def get_context_data(self, **kwargs):
        kwargs['user_type'] = 'Dog_Trainer'
        return super().get_context_data(**kwargs)
    
class OwnerSignUpView(CreateView):
    model = User
    form_class = OwnerForm
    template_name = 'auth/owner_reg.html'
    success_url =reverse_lazy('owner_login')

    def get_context_data(self, **kwargs):
        kwargs['user_type'] = 'Dog_Owner'
        return super().get_context_data(**kwargs)


def ownerloginView(request):
    form=OwnerLoginForm()
    if request.method=='POST':
        form=OwnerLoginForm(request.POST)
        if form.is_valid():
            username=form.cleaned_data['username']
            password=form.cleaned_data['password']
            user=authenticate(request,username=username,password=password)
            if user is not None:
                login(request,user)
                messages.success(request, username + " Logged In Successfully!")
                return redirect(index)
            else:
                messages.error(request, "Username or Password is Incorrect. Please Try Again!")
                return redirect(ownerloginView)
        else:
            return HttpResponse("Form is not Valid")
    
    return render(request,'auth/owner_login.html',locals())

def trainerloginView(request):
    form=TrainerLoginForm
    if request.method=='POST':
        form=TrainerLoginForm(request.POST)
        if form.is_valid():
            username=form.cleaned_data['username']
            password=form.cleaned_data['password']
            user=authenticate(request,username=username,password=password)
            if user is not None:
                login(request,user)
                messages.success(request, username + " Logged In Successfully!")
                return redirect(index)
            else:
                messages.error(request, "Username or Password is Incorrect. Please Try Again!")
                return redirect(trainerloginView)

                # return HttpResponse('Such a user does not exist')
        else:
            return HttpResponse("Form is Not Valid")
    
    return render(request,'auth/trainer_login.html',locals())

def logout_user(request):
    logout(request)
    messages.success(request,"User Logged Out Successfully!")
    return redirect(index)

@login_required(login_url='/accounts/login/owner')
def owner_profile(request, id):
    user=User.objects.filter(id=id).first()
    owner = Owner.objects.get(user=id)
    dogs=Dog.filter_by_user(user=owner.id)
    bookings=Booking.filter_by_owner(user=owner.id)
    
    uform=EditUserForm()
    form = OwnerProfileForm()
    dform = DogForm()
    if request.method == 'POST'and request.POST.get('form_type') == 'form':
        uform=EditUserForm(request.POST, instance=request.user)
        form=OwnerProfileForm(request.POST, request.FILES, instance=request.user.Dog_Owner)
        if uform.is_valid() and form.is_valid():
            user_form = uform.save()
            profile= form.save(commit=False)
            profile.user= user_form
            profile.save()

            messages.success(request, " Profile Updated Successfully!")
            return HttpResponseRedirect(request.path_info)
        else:
            messages.error(request, "Profile Updated Error! Please Try Again.")
            return HttpResponseRedirect(request.path_info)
    else:
        uform=EditUserForm()
        form=OwnerProfileForm()
        
    if request.method == 'POST'and request.POST.get('form_type') == 'dform':
        dform = DogForm(request.POST, request.FILES)
        if dform.is_valid():
            owner= dform.save(commit=False)
            owner.user= request.user.Dog_Owner
            owner.save()

            messages.success(request, "Dog Added Successfully!")
            return HttpResponseRedirect(request.path_info)

        else:
            messages.error(request, "Error! Please Try Again.")
            return HttpResponseRedirect(request.path_info)

    else:
        dform=DogForm()
    return render(request,'profile/owner_profile.html',locals())

@login_required(login_url='/accounts/login/trainer')
def trainer_profile(request, id):
    user=User.objects.filter(id=id).first()
    trainer = Trainer.objects.get(user=id)
    posts=Post.filter_by_user(user=trainer.id)
    reviews=Review.get_trainer_reviews(id=trainer.id)
    clinics=Clinic.filter_by_user(user=trainer.id)
    hours=Hours.filter_by_user(user=trainer.id).order_by("day")
    
    uform=EditUserForm()
    tform = TrainerProfileForm()
    hform=HoursForm()
    pform=PostForm()
    cform=ClinicForm()
    rform=ReviewForm()

    if request.method=='POST' and request.POST.get('form_type') == 'pform':
        pform = PostForm(request.POST, request.FILES)
        if pform.is_valid():
            print(pform.cleaned_data)
            post=pform.save(commit=False)
            post.user= request.user.Dog_Trainer
            post.save()

            messages.success(request, "Post Added Successfully!")
            return HttpResponseRedirect(request.path_info)
        else:
            messages.error(request, "Error! Please Try Again.")
            return HttpResponseRedirect(request.path_info)
    else:
        pform=PostForm()
        
    if request.method=='POST' and request.POST.get('form_type') == 'tform':
        uform=EditUserForm(request.POST, instance=request.user)
        tform = TrainerProfileForm(request.POST, request.FILES, instance=request.user.Dog_Trainer)
        if uform.is_valid() and tform.is_valid():
            user_form= uform.save()
            profile= tform.save(commit=False)
            profile.user= user_form
            profile.save()

            messages.success(request, " Profile Updated Successfully!")
            return HttpResponseRedirect(request.path_info)
        else:
            messages.error(request, "Profile Updated Error! Please Try Again.")
            return HttpResponseRedirect(request.path_info)
    else:
        tform=TrainerProfileForm()
        
    if request.method=='POST' and request.POST.get('form_type') == 'cform':
        cform = ClinicForm(request.POST, request.FILES)
        if cform.is_valid():
            print(cform.cleaned_data)
            clinic=cform.save(commit=False)
            clinic.user= request.user.Dog_Trainer
            clinic.save()

            messages.success(request, " Clinic Added Successfully!")
            return HttpResponseRedirect(request.path_info)

        else:
            messages.error(request, "Error! Please Try Again.")
            return HttpResponseRedirect(request.path_info)

    else:
        cform=ClinicForm()
    
    if request.method=='POST' and request.POST.get('form_type') == 'hform':
        hform = HoursForm(request.POST, request.FILES)
        if hform.is_valid():
            print(hform.cleaned_data)
            h=hform.save(commit=False)
            h.user=request.user.Dog_Trainer
            h.save()
            messages.success(request, " Business Hours Added Successfully!")
            return HttpResponseRedirect(request.path_info)

        else:
            messages.error(request, "Error! Please Try Again.")
            return HttpResponseRedirect(request.path_info)
    else:
        hform=HoursForm()
    
    if request.method=='POST' and request.POST.get('form_type') == 'rform':
        rform = ReviewForm(request.POST, request.FILES)
        if rform.is_valid():
            r=rform.save(commit=False)
            r.reviewer=request.user
            r.reviewed=trainer
            r.save()
            messages.success(request, "Trainer Reviewed Successfully!")
            return HttpResponseRedirect(request.path_info)

        else:
            messages.error(request, "Error! Please Try Again.")
            return HttpResponseRedirect(request.path_info)
    else:
        rform=ReviewForm()
    
    return render(request,'profile/trainer_profile.html',locals())

@login_required(login_url='/accounts/login/owner')
def booking(request, trainer_id):
    current_user= request.user.Dog_Owner
    current_trainer = Trainer.objects.get(id=trainer_id)
    if request.method == 'POST':
        form = BookingForm(request.POST, request.FILES)
        if form.is_valid():
            form = form.save(commit=False) 
            form.user=current_user 
            form.trainer=current_trainer
            form.save()

            messages.success(request, "Booking Added Successfully!")
            return HttpResponseRedirect(request.path_info)
            # return redirect(owner_profile)

        else:
            messages.error(request, "Error! Please Try Again.")
            return HttpResponseRedirect(request.path_info)
            # return redirect(index)
    else:
        form=BookingForm()
            
    return render(request,'booking.html',locals())

@login_required(login_url='/accounts/login/trainer')
def delete_hour(request, id):
  hour = Hours.objects.get(id=id)
  hour.delete()
  messages.success(request, "Business Hour Deleted Successfully!")
  current_user= request.user
  return redirect(trainer_profile, current_user.id)

@login_required(login_url='/accounts/login/trainer')
def delete_post(request, id):
  post = Post.objects.get(id=id)
  post.delete()
  messages.success(request, "Post Deleted Successfully!")
  current_user= request.user
  return redirect(trainer_profile, current_user.id)

@login_required(login_url='/accounts/login/owner')
def delete_review(request, id):
  review = Review.objects.get(id=id)
  review.delete()
  messages.success(request, "Review Deleted Successfully!")
  current_user= request.user
  return redirect(trainer_profile, current_user.id)

@login_required(login_url='/accounts/login/trainer')
def delete_clinic(request, id):
  clinic = Clinic.objects.get(id=id)
  clinic.delete()
  messages.success(request, "Clinic Deleted Successfully!")
  current_user= request.user
  return redirect(trainer_profile, current_user.id)

@login_required(login_url='/accounts/login/owner')
def delete_dog(request, id):
  dog = Dog.objects.get(id=id)
  dog.delete()
  messages.success(request, "Dog Deleted Successfully!")
  current_user= request.user
  return redirect(owner_profile, current_user.id)


# mpesa
def success(request):
  messages.success(request, "Transaction Successful!")
  current_user= request.user
  status=200
  return redirect(owner_profile, current_user.id)

def unsuccessful(request):
  messages.success(request, "Unsuccessful Transaction, Please Try again later.!")
  current_user= request.user
  return redirect(owner_profile, current_user.id)

@login_required(login_url='/accounts/login/owner')
def lipa_na_mpesa_online(request, trainer_id):
    current_user = request.user
    current_trainer = Trainer.objects.get(id=trainer_id)
    access_token = MpesaAccessToken.validated_mpesa_access_token
    api_url = "https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest"
    headers = {"Authorization": "Bearer %s" % access_token}
    request = {
        "BusinessShortCode": LipanaMpesaPpassword.Business_short_code,
        "Password": LipanaMpesaPpassword.decode_password,
        "Timestamp": LipanaMpesaPpassword.lipa_time,
        "TransactionType": "CustomerPayBillOnline",
        "Amount": current_trainer.price_charge,
        "PartyA": current_user.phone,  # replace with your phone number to get stk push
        "PartyB": LipanaMpesaPpassword.Business_short_code,
        "PhoneNumber": current_user.phone,  # replace with your phone number to get stk push
        "CallBackURL": "https://sandbox.safaricom.co.ke/mpesa/",
        "AccountReference": current_trainer.user.username,
        "TransactionDesc": "Testing stk push"
    }
    response = requests.post(api_url, json=request, headers=headers)
    if response.status_code==200:
        return redirect(success)
    else:
        return redirect(unsuccessful)