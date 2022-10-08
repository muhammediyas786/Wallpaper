from django.urls import path
from . import views

SOCIAL_AUTH_URL_NAMESPACE = 'social'
urlpatterns = [
    path('',views.home,name='home'),
    path('login/',views.login,name='login'),
    path('signup/',views.signup,name='signup'),
    path('logout/',views.logout,name='logout'),
    path('upload/',views.details,name='upload'),
    path('profile/',views.profile,name='profile'),
    path('more/',views.streams,name='more'),
    path('search/',views.search,name='search'),
    path('delete/<str:pk>/',views.delete,name='delete'),
    path('users_profile/<str:pk>/',views.users_profile,name='users_profile'),
    path('<slug:category_slug>/',views.home,name='category_slug'),
    
    
]