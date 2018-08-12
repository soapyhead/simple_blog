from django.urls import path
from .views import (
    UserView, CreateUserView, LoginUserView, LogoutUserView
)

urlpatterns = [
    path('sign_up/', CreateUserView.as_view(), name='sign_up'),
    path('login/', LoginUserView.as_view(), name='login'),
    path('logout/', LogoutUserView.as_view(), name='logout'),
    path('profile/', UserView.as_view(), name='profile'),
]