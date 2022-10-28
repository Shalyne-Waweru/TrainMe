from django.urls import include, path

from . import views

urlpatterns = [
    path('accounts/', include('django.contrib.auth.urls')),
    path('accounts/signup/', views.index, name='signup'),
    path('accounts/signup/trainer/', views.TrainerSignUpView.as_view(), name='trainer_signup'),
    path('accounts/signup/owner/', views.OwnerSignUpView.as_view(), name='owner_signup'),
    
    path('login/', views.loginView),
    # path('logout/', views.logout_user),
    path('dogadd/<id>', views.dog, name='dog_form'),
    path('addpost/<id>', views.post, name='post_form'),
    path('addreview/<id>', views.review, name='review_form'),
]
