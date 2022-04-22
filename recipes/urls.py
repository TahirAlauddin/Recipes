from django.urls import path
from . import views

urlpatterns = [
    path("create-recipe/", views.view_create_recipe, name="create-recipe"),
    path("create-ingredient/", views.view_create_ingredient, name="create-ingredient"),
    path("create-utensil/", views.view_create_utensil, name="create-utensil"),
    path("recipe-detail/<str:slug>/", views.view_recipe_detail, name="recipe-detail"),
    path("", views.view_home, name="home"),
]