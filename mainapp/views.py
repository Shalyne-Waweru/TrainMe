from django.shortcuts import render
from django.views.generic import CreateView

from accounts.forms import TrainerForm, OwnerForm
from accounts.models import User

# Create your views here.

def index(request):
    return render(request, 'auth/index.html',locals())

class TrainerSignUpView(CreateView):
    model = User
    form_class = TrainerForm
    template_name = 'auth/trainer_reg.html'

    def get_context_data(self, **kwargs):
        kwargs['user_type'] = 'Dog_Trainer'
        return super().get_context_data(**kwargs)
    
class OwnerSignUpView(CreateView):
    model = User
    form_class = OwnerForm
    template_name = 'auth/owner_reg.html'

    def get_context_data(self, **kwargs):
        kwargs['user_type'] = 'Dog_Owner'
        return super().get_context_data(**kwargs)
