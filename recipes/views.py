from django.shortcuts import render
from .models import *

def home(request):
    return render(request, "recipes/list_recipes.html")


def create_recipe(request):
    if request.method == 'POST':
        # Create Recipe
        # for filename, file in request.FILES.iteritems():
        #     name = request.FILES[filename].name
        form = request.POST
        images = request.FILES.getlist('images')
        title = form.get('title')
        description = form.get('description')
        prep_time = form.get('prep_time')
        difficulty = form.get('difficulty')
        cost = form.get('cost')
        number_of_dishes = form.get('dishes')
        category = form.get('category')

        ingredients_quantity = form.getlist('ingredients-quantity')
        ingredients_name = form.getlist('ingredients-name')
        utensils_quantity = form.getlist('utensils-quantity')
        utensils_name = form.getlist('utensils-name')

        recipe = Recipe(title=title, description=description, cost=cost,
                        difficulty=difficulty, preparation_time=prep_time)
        for image in images:
            recipeImage = RecipeImage(image=image, recipe=Recipe)


        for ingredients_name, ingredient_quantity in zip(ingredients_name, ingredients_quantity):
            ingredientItem = IngredientItem(name=ingredient_name, quantity=ingredient_quantity,
                                            recipe=Recipe)


        for utensil_name, utensil_item in zip(utensils_name, utensils_quantity):
            utensilItem = UtensilItem(name=utensil_name, quantity=utensil_quantity,
                                            recipe=Recipe)



    return render(request, "recipes/create_recipe.html")

