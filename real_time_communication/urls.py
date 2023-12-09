from django.urls import path, include
from .routes import getRoutes

urlpatterns = [
    path('', getRoutes, name='routes'),
    path('auth/', include('authentication.urls')),
    path('products/', include('products.urls')),
]
