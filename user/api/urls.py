from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token

from rest_framework_simplejwt.views import(
    TokenObtainPairView,
    TokenRefreshView
)

from user.api import views

urlpatterns = [
    path('login/', obtain_auth_token, name='login'),
    path('register/', views.user_registration_view, name='register'),
    path('logout/', views.logout_view, name='logout'),

    # For JWT token
    # path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    # path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
