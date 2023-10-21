from django.urls import path
from restaurant import views

app_name = 'restaurant'

urlpatterns = [
    path('restaurant', views.restaurant, name="restaurant"),
    path('menu', views.menu, name="menu"),
    path('menu-vote', views.menu_vote, name="menu-vote"),
]
