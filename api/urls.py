from django.urls import path
from api import views


urlpatterns = [
    path('v2/characters', views.characters, name='v2_characters'),
    path('v2/populate_db', views.PopulateDB.as_view(), name='v2_populate_db'),
]
