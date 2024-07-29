from api import views
from django.urls import path, re_path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView



urlpatterns = [
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('v2/characters', views.characters, name='v2_characters'),
    path('v2/importdata', views.ImportData.as_view(), name='v2_import_data'),
    re_path(r"^v2/tag/(?P<name>.*?)?$", views.GenericView.as_view(), name='tag'),
    re_path(r"^v2/tagset/(?P<name>.*?)?$", views.GenericView.as_view(), name='tagset'),
    re_path(r"^v2/community/(?P<name>.*?)?$", views.GenericView.as_view(), name='community'),
    re_path(r"^v2/communityuser/(?P<name>.*?)?$", views.GenericView.as_view(), name='communityuser'),
]
