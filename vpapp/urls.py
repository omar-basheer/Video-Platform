from django.urls import path
from .views import CreateUser, LoginUser, PasswordResetRequestView, PasswordResetView

urlpatterns = [
  path('signup/', CreateUser.as_view(), name='signup'),
  path('login/', LoginUser.as_view(), name='login'),
  path('request-password-reset/', PasswordResetRequestView.as_view(), name='request-password-reset'),
  path('reset-password/', PasswordResetView.as_view(), name='reset-password'),
]