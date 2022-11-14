from django.shortcuts import render, redirect, HttpResponse, HttpResponseRedirect
from django.views.generic import CreateView

from accounts.forms import OwnerLoginForm, TrainerForm, OwnerForm, TrainerLoginForm, TrainerProfileForm
from accounts.models import Owner, Trainer, User
# from accounts.choices import service

from django.contrib.auth import login,authenticate, logout
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required

from mainapp.forms import BookingForm, DogForm, PostForm, ReviewForm, HoursForm,ServiceForm
from mainapp.models import Booking, Hours, Clinic, Post, Review, Service

# Create your views here.
def index(request):
    trainers= Trainer.objects.all()
    return render(request, 'index.html',locals())

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
    if request.method == 'POST':
        form = DogForm(request.POST, request.FILES)
        if form.is_valid():
            owner= form.save(commit=False)
            owner.user= request.user
            owner.save()
            return HttpResponseRedirect(request.path_info)
    else:
        form=DogForm()
    return render(request,'profile/owner_profile.html',locals())

def trainer_profile(request, id):
    user=User.objects.filter(id=id).first()
    trainer = Trainer.objects.get(user=id)
    posts=Post.filter_by_user(user=trainer.id)
    reviews=Review.get_trainer_reviews(id=trainer.id)
    clinics=Clinic.filter_by_user(user=trainer.id)
    hours=Hours.filter_by_user(user=trainer.id)
    print(hours)
    bookings=Booking.filter_by_trainer(id=trainer.id)
    owner = request.user.Dog_Trainer
    current_trainer = Trainer.objects.get(user=id)
    
    form = TrainerProfileForm()
    hform=HoursForm()
    pform=PostForm()
    sform=ServiceForm()
    # if request.POST.get('form_type') == 'pform':
    #     pform = PostForm(request.POST, request.FILES, instance=request.user.Dog_Trainer)
    #     if pform.is_bound():
    #         if pform.is_valid():
    #             print(pform.cleaned_data)
    #             # post=pform.save(commit=False)
    #             # post.user= request.user
    #             pform.save()
    #     return HttpResponse('pform')
    # if request.POST.get('form_type') == 'form':
    #     form = TrainerProfileForm(request.POST, request.FILES, instance=request.user.Dog_Trainer)
    #     if form.is_valid():
    #         print(form.cleaned_data)
    #         profile= form.save(commit=False)
    #         profile.user= request.user
    #         clinic = Clinic.objects.create(user=owner)
    #         clinic.clinic_name= form.cleaned_data.get('clinic_name')
    #         clinic.clinic_location= form.cleaned_data.get('clinic_location')
    #         profile.save()
    #         clinic.save()
    #     return HttpResponse('form')
    if request.method=='POST' and request.POST.get('form_type') == 'hform':
        hform = HoursForm(request.POST, request.FILES, instance=request.user.Dog_Trainer)
        if hform.is_valid():
            print(hform.cleaned_data)
            h=hform.save(commit=False)
            h.user=request.user
            h.save()
            return HttpResponse('hform')
        else:
            hform=HoursForm()
    # if request.POST.get('form_type') == 'sform':
    #     sform = ServiceForm(request.POST, request.FILES, instance=request.user.Dog_Trainer)
    #     if sform.is_valid():
    #         service = Service.objects.create(user=owner)
    #         service.services=sform.cleaned_data.get('services')
    #         service.save()
    #     return HttpResponse('sform')
    
    return render(request,'profile/trainer_profile.html',locals())

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
