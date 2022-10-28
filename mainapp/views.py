from django.shortcuts import render, redirect, HttpResponse
from django.views.generic import CreateView

from accounts.forms import LoginForm, TrainerForm, OwnerForm
from accounts.models import Owner, Trainer, User

from django.contrib.auth import login,authenticate, logout
from django.urls import reverse_lazy

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


def loginView(request):
    form=LoginForm()
    if request.method=='POST':
        form=LoginForm(request.POST)
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
    
    return render(request,'auth/login.html',locals())