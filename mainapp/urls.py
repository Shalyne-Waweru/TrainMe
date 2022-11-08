from django.urls import include, path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    
    path('accounts/', include('django.contrib.auth.urls')),
    # path('accounts/signup/', views.signup, name='signup'),
    path('accounts/signup/trainer/', views.TrainerSignUpView.as_view(), name='trainer_signup'),
    path('accounts/signup/owner/', views.OwnerSignUpView.as_view(), name='owner_signup'),
    # path('login/', views.loginView, name='login'),
    path('accounts/login/trainer', views.trainerloginView, name='trainer_login'),
    path('accounts/login/owner', views.ownerloginView, name='owner_login'),
    path('logout/', views.logout_user, name='logout'),
    
    path('profile/trainer/<id>', views.trainer_profile, name='trainer_profile'),
    path('profile/owner/<id>', views.owner_profile, name='owner_profile'),
    
    path('dogadd/<id>', views.dog, name='dog_form'),
    # path('addpost/<id>', views.post, name='post_form'),
    path('addreview/<trainer_id>', views.review, name='review_form'),
    path('book/<trainer_id>', views.booking, name='booking_form'),

    # Index/Landing Page
    path('', views.index, name='landingPage'),
    # Search Page
    path('search/', views.search, name='searchPage'),
    path('gender/', views.gender, name='gender'),
]
