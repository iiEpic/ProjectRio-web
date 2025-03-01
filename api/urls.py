from api import views
from django.urls import path, re_path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView


app_name = 'api'
urlpatterns = [
    # ----- Start v2 Endpoints ----- #
    path('v2/populatedb/', views.PopulateDB.as_view(), name='populatedb'),
    path('v2/tag/', views.Tag.as_view(), name='tag_list'),
    path('v2/tagset/', views.TagSet.as_view(), name='tagset_list'),
    path('v2/gamemode/', views.TagSet.as_view(), name='gamemode_list'),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
