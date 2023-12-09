from django.urls import path
from .views import RegistrationView, LoginView, LogoutView, getRoutes


urlpatterns = [
    path('', LoginView.as_view(), name='auth'),
    path('register/', RegistrationView.as_view(), name='routes'),
    path('logout/', LogoutView.as_view(), name='logout'),
]
