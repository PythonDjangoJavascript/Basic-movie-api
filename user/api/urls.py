from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token

from user.api import views

urlpatterns = [
    path('login/', obtain_auth_token, name='login'),
    path('register/', views.user_registration_view, name='register'),
]
