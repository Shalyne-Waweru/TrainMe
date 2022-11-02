from django.shortcuts import render, redirect, HttpResponse, HttpResponseRedirect
from django.views.generic import CreateView

from accounts.forms import OwnerLoginForm, TrainerForm, OwnerForm, TrainerLoginForm, TrainerProfileForm
from accounts.models import Owner, Trainer, User
from accounts.choices import services

from django.contrib.auth import login,authenticate, logout
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required

from mainapp.forms import BookingForm, ClinicForm, DogForm, HoursForm, PostForm, ReviewForm
from mainapp.models import Booking, BusinessHours, Clinic, Post, Review

# Create your views here.
def index(request):
    trainers= Trainer.objects.all()
    return render(request, 'index.html',locals())

def signup(request):
    return render(request, 'auth/signup.html',locals())

def loginView(request):
    return render(request, 'auth/login.html',locals())

def search(request):
    servs= services
    return render(request, 'search.html', locals())

class TrainerSignUpView(CreateView):
    model = User
    form_class = TrainerForm
    template_name = 'auth/trainer_reg.html'
    success_url =reverse_lazy('signup')

    def get_context_data(self, **kwargs):
        kwargs['user_type'] = 'Dog_Trainer'
        return super().get_context_data(**kwargs)
    
class OwnerSignUpView(CreateView):
    model = User
    form_class = OwnerForm
    template_name = 'auth/owner_reg.html'
    success_url =reverse_lazy('signup')

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
                return redirect(index)
            else:
                return HttpResponse('Such a user does not exist')
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
                return redirect(index)
            else:
                return HttpResponse('Such a user does not exist')
        else:
            return HttpResponse("Form is not Valid")
    
    return render(request,'auth/trainer_login.html',locals())

def logout_user(request):
    logout(request)
    return redirect(index)

def owner_profile(request, id):
    user=User.objects.filter(id=id).first()
    owner = Owner.objects.get(user=id)
    return render(request,'profile/owner_profile.html',locals())

def trainer_profile(request, id):
    user=User.objects.filter(id=id).first()
    trainer = Trainer.objects.get(user=id)
    posts=Post.filter_by_user(user=trainer.id)
    reviews=Review.get_trainer_reviews(id=trainer.id)
    clinics=Clinic.filter_by_user(user=trainer.id)
    hours=BusinessHours.filter_by_user(user=trainer.id)
    bookings=Booking.filter_by_trainer(id=trainer.id)
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES, instance=request.user.Dog_Trainer)
        pform = TrainerProfileForm(request.POST, request.FILES, instance=request.user.Dog_Trainer)
        cform=ClinicForm(request.POST, request.FILES, instance=request.user.Dog_Trainer)
        hform=HoursForm(request.POST, request.FILES, instance=request.user.Dog_Trainer)
        if form.is_valid():
            t= form.save(commit=False)
            t.user= request.user
            t.save()
            return HttpResponseRedirect(request.path_info)
        elif pform.is_valid():
            p= pform.save(commit=False)
            p.user= request.user
            p.save()
            return HttpResponseRedirect(request.path_info)
        elif cform.is_valid():
            c= cform.save(commit=False)
            c.user= request.user
            c.save()
            return HttpResponseRedirect(request.path_info)
        elif hform.is_valid():
            h= hform.save(commit=False)
            h.user= request.user
            h.save()
            return HttpResponseRedirect(request.path_info)
    else:
        form=PostForm()
        pform = TrainerProfileForm()
        cform=ClinicForm()
        hform=HoursForm()
    return render(request,'profile/trainer_profile.html',locals())

def dog(request, id):
    user=User.objects.filter(id=id).first()
    owner = Owner.objects.get(user=id)
    if request.method == 'POST':
        form = DogForm(request.POST, request.FILES)
        if form.is_valid():
            owner= form.save(commit=False)
            owner.user= request.user
            owner.save()
            return redirect(index)
    else:
        form=DogForm()
            
    return render(request,'dog_form.html',locals())

@login_required(login_url='/login')
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
            
            return redirect(index)
    else:
        form=ReviewForm()
            
    return render(request,'review_form.html',locals())

@login_required(login_url='/login')
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
