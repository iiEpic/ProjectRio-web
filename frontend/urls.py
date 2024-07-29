from django.urls import path, re_path
from frontend import views


app_name = 'frontend'
urlpatterns = [
    path('', views.Home.as_view(), name='home'),
    path('login', views.Login.as_view(), name='login'),
    path('logout', views.Logout.as_view(), name='logout'),
    path('register', views.Register.as_view(), name='register'),
    re_path(r"^communities/(?P<name>.*?)?$", views.Communities.as_view(), name='communities'),
    re_path(r"^users/(?P<username>.*?)/batting$", views.UserBatting.as_view(), name='user_batting'),
    re_path(r"^users/(?P<username>.*?)/pitching$", views.UserPitching.as_view(), name='user_pitching'),
    re_path(r"^users/(?P<username>.*?)?$", views.Users.as_view(), name='users'),
]
