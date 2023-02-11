from django.urls import path, include
from .views import *


urlpatterns = [
    path('api/', include('app.api.urls')),
    path('login/', LoginView.as_view(), name='login'),
    path('register/', RegisterView.as_view(), name='register'),
    path('logout/', LogoutView.as_view(), name='logout'),
]