from django.shortcuts import render, redirect, HttpResponse
from django.views.generic import CreateView

from accounts.forms import OwnerLoginForm, TrainerForm, OwnerForm, TrainerLoginForm
from accounts.models import Owner, Trainer, User

from django.contrib.auth import login,authenticate, logout
from django.urls import reverse_lazy

from mainapp.forms import DogForm, PostForm, ReviewForm

# Create your views here.

def index(request):
    return render(request, 'auth/index.html',locals())

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

def post(request, id):
    user=User.objects.filter(id=id).first()
    trainer = Trainer.objects.get(user=id)
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            trainer= form.save(commit=False)
            trainer.user= request.user
            trainer.save()
            return redirect(index)
    else:
        form=PostForm()
            
    return render(request,'post_form.html',locals())

def review(request, trainer_id):
    current_user = request.user
    current_trainer = Trainer.objects.get(id=trainer_id)
    if request.method == 'POST':
        form = ReviewForm(request.POST, request.FILES)
        if form.is_valid():
            form = form.save(commit=False) 
            form.user=current_user 
            form.image=current_trainer
            form.save()
            
            return redirect(index)
    else:
        form=ReviewForm()
            
    return render(request,'review_form.html',locals())