from django.urls import path, re_path
from frontend import views


app_name = 'frontend'
urlpatterns = [
    path('', views.Home.as_view(), name='home'),
    path('login/', views.Login.as_view(), name='login'),
    path('logout/', views.Logout.as_view(), name='logout'),
    path('register/', views.Register.as_view(), name='register'),

    # Gamemodes (TagSet)
    path("gamemode/", views.Tagsets.as_view(), name='gamemode_list'),
    path("gamemode/create/", views.Tagsets.as_view(), name='gamemode_create'),
    path("gamemode/<str:slug>/", views.Tagsets.as_view(), name='gamemode_detail'),

    # Tags
    path('tag/', views.TagList.as_view(), name='tag_list'),
    path('tag/create/', views.TagCreate.as_view(), name='tag_create'),
    path('tag/<str:slug>/delete/', views.TagDelete.as_view(), name='tag_delete'),
    path('tag/<str:slug>/edit/', views.TagEdit.as_view(), name='tag_edit'),
    path('tag/<str:slug>/', views.TagList.as_view(), name='tag_detail'),

    # Communities
    path('community/', views.Community.as_view(), name='community_list'),
    path('community/create/', views.Community.as_view(), name='community_create'),
    # path('communities/create/', views.CreateCommunity.as_view(), name='create_community'),
    path('community/<str:slug>/', views.Community.as_view(), name='community_detail'),

    # Users
    path('users/', views.Users.as_view(), name='user_list'),
    path('users/<str:username>', views.Users.as_view(), name='user_detail'),

    # REVIEW: Below this line are paths that need to be updated to new standard
    re_path(r"^users/(?P<username>.*?)/batting/$", views.UserBatting.as_view(), name='user_batting'),
    re_path(r"^users/(?P<username>.*?)/pitching/$", views.UserPitching.as_view(), name='user_pitching')
]
