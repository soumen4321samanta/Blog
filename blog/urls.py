from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('',views.home,name='home'),
    path('signup',views.signup,name='signup'),
    path('signin',views.signin,name='signin'),
    path('signout',views.signout,name='signout'),
    path('token_send',views.token_send,name='token_send'),
    path('success',views.success,name='success'),
    path('verify/<str:auth_token>/', views.verify, name='verify'),
    path('error',views.error,name='error'),
    path('about/',views.about,name='about'),
    path('contact',views.contact,name='contact'),
    path('request-reset-password/', views.request_reset_password, name='request_reset_password'),
    path('reset-password/<uidb64>/<token>/', views.reset_password, name='reset_password'),


    path('list/',views.tweet_list,name='tweet_list'),
    path('signin/', auth_views.LoginView.as_view(template_name='signin.html'), name='login'),

    path('create/',views.tweet_create,name='tweet_create'),

    path('<int:tweet_id>/edit/',views.tweet_edit,name='tweet_edit'),

    path('<int:tweet_id>/delete/',views.tweet_delete,name='tweet_delete'),

    path('dashboard/', views.user_dashboard, name='user-dashboard'),
    path('profile/', views.profile_view, name='profile'),

    path('change-password',views.custom_change_password,name="custom_change_password"),

    
    
    
]