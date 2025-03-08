from api import views
from django.urls import path, re_path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView


app_name = 'api'
urlpatterns = [
    # ----- Start v2 Endpoints ----- #
    # Create paths
    path('v2/tags/create/', views.TagCreate.as_view(), name='tag-create'),

    # Detailed paths
    path('v2/usergroups/<int:pk>/', views.UserGroupDetail.as_view(), name='usergroup-detail'),
    path('v2/userprofiles/<int:pk>/', views.UserProfileDetail.as_view(), name='userprofile-detail'),
    path('v2/characters/<str:identifier>/', views.CharacterDetail.as_view(), name='character-detail'),
    path('v2/characterchemistries/<int:pk>/', views.CharacterChemistryDetail.as_view(),
         name='characterchemistry-detail'),
    path('v2/communities/<int:pk>/', views.CommunityDetail.as_view(), name='community-detail'),
    path('v2/roles/<int:pk>/', views.RoleDetail.as_view(), name='role-detail'),
    path('v2/communityusers/<int:pk>/', views.CommunityUserDetail.as_view(), name='communityuser-detail'),
    path('v2/tags/<int:pk>/', views.TagDetail.as_view(), name='tag-detail'),
    path('v2/tagsets/<int:pk>/', views.TagSetDetail.as_view(), name='tagset-detail'),
    path('v2/games/<int:pk>/', views.GameDetail.as_view(), name='game-detail'),
    path('v2/gamerosters/<int:pk>/', views.GameRosterDetail.as_view(), name='gameroster-detail'),
    path('v2/gameeventsummaries/<int:pk>/', views.GameEventSummaryDetail.as_view(), name='gameeventsummary-detail'),
    path('v2/gameevents/<int:pk>/', views.GameEventDetail.as_view(), name='gameevent-detail'),
    path('v2/ladders/<int:pk>/', views.LadderDetail.as_view(), name='ladder-detail'),

    # List paths
    path('v2/usergroups/', views.UserGroupList.as_view(), name='usergroup-list'),
    path('v2/userprofiles/', views.UserProfileList.as_view(), name='userprofile-list'),
    path('v2/characters/', views.CharacterList.as_view(), name='character-list'),
    path('v2/characterchemistries/', views.CharacterChemistryList.as_view(), name='characterchemistry-list'),
    path('v2/communities/', views.CommunityList.as_view(), name='community-list'),
    path('v2/roles/', views.RoleList.as_view(), name='role-list'),
    path('v2/communityusers/', views.CommunityUserList.as_view(), name='communityuser-list'),
    path('v2/tags/', views.TagList.as_view(), name='tag-list'),
    path('v2/tagsets/', views.TagSetList.as_view(), name='tagset-list'),
    path('v2/games/', views.GameList.as_view(), name='game-list'),
    path('v2/gamerosters/', views.GameRosterList.as_view(), name='gameroster-list'),
    path('v2/gameeventsummaries/', views.GameEventSummaryList.as_view(), name='gameeventsummary-list'),
    path('v2/gameevents/', views.GameEventList.as_view(), name='gameevent-list'),
    path('v2/ladders/', views.LadderList.as_view(), name='ladder-list'),

    # Misc
    path('v2/populatedb/', views.PopulateDB.as_view(), name='populatedb'),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
