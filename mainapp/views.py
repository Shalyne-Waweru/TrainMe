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

# Create your views here.
def index(request):
    trainers= Trainer.objects.all()
    return render(request, 'index.html',locals())

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
    if request.method == 'POST':
        form = DogForm(request.POST, request.FILES)
        if form.is_valid():
            owner= form.save(commit=False)
            owner.user= request.user.Dog_Owner
            owner.save()
            return HttpResponseRedirect(request.path_info)
    else:
        form=DogForm()
    return render(request,'profile/owner_profile.html',locals())

@login_required(login_url='/accounts/login/owner')
def trainer_profile(request, id):
    user=User.objects.filter(id=id).first()
    trainer = Trainer.objects.get(user=id)
    posts=Post.filter_by_user(user=trainer.id)
    reviews=Review.get_trainer_reviews(id=trainer.id)
    clinics=Clinic.filter_by_user(user=trainer.id)
    hours=Hours.filter_by_user(user=trainer.id).order_by("day")
    bookings=Booking.filter_by_trainer(id=trainer.id)
    
    tform = TrainerProfileForm()
    hform=HoursForm()
    pform=PostForm()
    cform=ClinicForm()

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
        tform = TrainerProfileForm(request.POST, request.FILES, instance=request.user.Dog_Trainer)
        if tform.is_valid():
            print(tform.cleaned_data)
            profile= tform.save(commit=False)
            profile.user= request.user
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
    
    return render(request,'profile/trainer_profile.html',locals())

@login_required(login_url='/accounts/login/owner')
def review(request, trainer_id):
    current_user = request.user
    current_trainer = Trainer.objects.get(id=trainer_id)
    if request.method == 'POST':
        form = ReviewForm(request.POST, request.FILES)
        if form.is_valid():
            form = form.save(commit=False) 
            form.reviewer=current_user 
            form.reviewed=current_trainer
            form.save()
            
            # return redirect('trainer_profile')
            return HttpResponseRedirect(request.path_info)
    else:
        form=ReviewForm()
            
    return render(request,'review_form.html',locals())

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
            return redirect(index)
    else:
        form=BookingForm()
            
    return render(request,'booking.html',locals())

def delete_hour(request, id):
  hour = Hours.objects.get(id=id)
  hour.delete()
  return redirect(index)

def delete_post(request, id):
  post = Post.objects.get(id=id)
  post.delete()
  return redirect(index)

def delete_booking(request, id):
  booking = Booking.objects.get(id=id)
  booking.delete()
  return redirect(index)

def delete_review(request, id):
  review = Review.objects.get(id=id)
  review.delete()
  return redirect(index)

def delete_clinic(request, id):
  clinic = Clinic.objects.get(id=id)
  clinic.delete()
  return redirect(index)

def delete_dog(request, id):
  dog = Dog.objects.get(id=id)
  dog.delete()
  return redirect(index)