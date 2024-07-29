from django.urls import path
from api import views


urlpatterns = [
    path('v2/characters', views.characters, name='v2_characters'),
    path('v2/importdata', views.ImportData.as_view(), name='v2_import_data'),
]
