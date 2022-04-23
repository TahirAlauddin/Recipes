from django.shortcuts import render
from django.http import JsonResponse
from .models import *
from datetime import time

def view_home(request):
    recipes = Recipe.objects.all().order_by('?')[:10]
    context = {'recipes': recipes}

    return render(request, "recipes/index.html", context)


def view_create_recipe(request):
    if request.method == 'POST':
        # Create Recipe
        # for filename, file in request.FILES.iteritems():
        #     name = request.FILES[filename].name
        form = request.POST
        images = request.FILES.getlist('images')

        category_name = form.get('category')
        ingredients_quantity = form.getlist('ingredients-quantity')
        ingredients_name = form.getlist('ingredients-name')
        utensils_quantity = form.getlist('utensils-quantity')
        utensils_name = form.getlist('utensils-name')

        category = Category.objects.get(name=category_name)
        
        # Create a recipe object with form data
        recipe = Recipe(title=form.get('title'), description=form.get('description'),

                        cost=form.get('cost'), difficulty=form.get('difficulty'),

                        num_of_dishes=form.get('dishes'), category=category,

                        preparation_time=time(hour=form.get('prep_hours'),
                                            minute=form.get('prep_minutes')),
                        cooking_time=time(hour=form.get('cooking_hours'),
                                            minute=form.get('cooking_minutes')),
                        rest_time = time(hour=form.get('rest_hours'),
                                            minute=form.get('rest_minutes')),
                        )
        recipe.save()

        # Add images to the recipe
        for image in images:
            RecipeImage(image=image, recipe=Recipe).save()

        for ingredients_name, ingredient_quantity in zip(ingredients_name, ingredients_quantity):
            # Create a IngredientItem object and save it to the database
            IngredientItem(name=ingredient_name, quantity=ingredient_quantity,
                                            recipe=Recipe).save()

        for utensil_name, utensil_item in zip(utensils_name, utensils_quantity):
            # Create a UtensilItem object and save it to the database
            UtensilItem(name=utensil_name, quantity=utensil_quantity,
                                            recipe=Recipe).save()
    ingredients = Ingredient.objects.all()
    utensils = Utensil.objects.all()
    context = {'ingredients': ingredients, 'utensils': utensils}
    return render(request, "recipes/add_recipe.html", context=context)


def view_create_ingredient(request):
    if request.method == "POST":
        form = request.POST
        name = form.get('name')
        unit = form.get('unit')
        image = form.FILES.get('image')
    return render(request, "recipes/add_ingredients.html")



def view_create_utensil(request):
    if request.method == "POST":
        form = request.POST
        name = form.get('name')
        image = form.FILES.get('image')
    return render(request, "recipes/add_utensils.html")



def view_recipe_detail(request, slug):
    recipe = Recipe.objects.get(slug=slug)
    ingredients = recipe.ingredients.all()
    utensils = recipe.utensils.all()
    context = {'recipe': recipe, 'ingredientItems': ingredients, 'utensilItems': utensils} 
    return render(request, "recipes/recipe_detail.html", context=context)


def get_ingredients_quantity_api_view(request, slug, current_num_of_dishes):
    recipe = Recipe.objects.get(slug=slug)
    print(current_num_of_dishes)
    quantities = recipe.get_quantity_of_ingredients_from_number_of_dishes(current_num_of_dishes)
    return JsonResponse(quantities, safe=False)


def view_category(request):
    categories = Category.objects.all()
    context = {'categories': categories}
    return render(request, 'recipes/category.html', context=context)


def view_category_detail(request, slug):
    category = Category.objects.get(slug=slug)
    context = {'category': category}
    return render(request, 'recipes/category_detail.html', context=context)