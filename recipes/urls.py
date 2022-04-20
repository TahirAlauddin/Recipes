from django.urls import path
from . import views

urlpatterns = [
    path("create-recipe/", views.create_recipe, name="create-recipe"),
    path("", views.home, name="home"),
]