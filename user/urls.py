from django.urls import path
from django.contrib.auth import views as auth_views

from . import views

app_name = 'user'

urlpatterns = [
    path('register/', views.RegisterView.as_view(), name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('user/<str:username>/', views.UserDetails.as_view(), name='user_details'),
    path('book/<int:pk>/review/', views.CreateReview.as_view(), name='add_review'),
    ]
