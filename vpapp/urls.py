from django.urls import path
from .views import CreateUser, LoginUser

urlpatterns = [
  path('signup/', CreateUser.as_view(), name='signup'),
  path('login/', LoginUser.as_view(), name='login'),

]