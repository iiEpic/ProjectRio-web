from django.urls import path
from frontend import views


urlpatterns = [
    path('', views.Home.as_view(), name='home'),
    path('register', views.Register.as_view(), name='register'),
]
