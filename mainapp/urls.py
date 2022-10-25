from django.urls import include, path

from . import views

urlpatterns = [
    path('accounts/', include('django.contrib.auth.urls')),
    path('accounts/signup/', views.index, name='signup'),
    path('accounts/signup/trainer/', views.TrainerSignUpView.as_view(), name='trainer_signup'),
    path('accounts/signup/owner/', views.OwnerSignUpView.as_view(), name='owner_signup'),
]
