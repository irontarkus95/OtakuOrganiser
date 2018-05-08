from django.conf.urls import url
from django.urls import path
from .animes import Anime
from .import views
from .views import register
from django.contrib.auth import views as auth_views
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login

urlpatterns = [
    path('anime/register/', views.register, name = "register"),
    path('', views.full_anime_listing, name = 'anime_full_list'),
    path('anime/new/', views.add_anime, name = 'anime_new'),
    path('anime/details/<int:pk>/', views.view_animedetails, name = 'anime_details' ),
    path('anime/new/csv/', views.upload_csv, name = 'upload_csv' ),
    path('anime/login/', auth_views.login, name = 'login'),
    path('anime/logout-site/', views.logout_site, name = 'logout-site'),
    path('logout/', auth_views.logout, {'next_page': '/account/anime/logout-site'},  name='logout'),
    path('delete/<int:pk>/', views.delete, name = 'delete'),
    path('update/<int:anime_id>/', views.update, name = 'update'),
    path('search/', views.search, name = 'search'),
    path('404/', views.error404, name = '404')
] 

