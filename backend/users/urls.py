from django.urls import path
from .views import CustomUserRegister, BlacklistTokenUpdateView, CustomTokenObtainPairView
from rest_framework_simplejwt.views import TokenRefreshView

app_name = 'users'

urlpatterns = [
    path('register/', CustomUserRegister.as_view(), name="create_user"),
    path('login/', CustomTokenObtainPairView.as_view(), name="auth_user"),
    path('logout/', BlacklistTokenUpdateView.as_view(), name="deauth_user"),
    path('refresh/', TokenRefreshView.as_view(), name="token_refresh"),
]
