from django.urls import path
from django.contrib.auth import views as auth_views
#from project.settings import MEDIA_ROOT
from . import views

urlpatterns = [
    path('', views.home_action, name='home'),
    path('add_picture', views.add_picture_action, name='add_picture'),
    path('select', views.select_action, name='select'),
    path('photo/<int:id>', views.get_photo, name='photo'),
    #path('add_profile', views.add_post, name= "add_profile"),
    #path('add_follow/<int:id>', views.add_follow, name= "add_follow"),
]