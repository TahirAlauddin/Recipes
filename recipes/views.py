from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages 
from django.conf import settings
from django.contrib.auth import get_user_model
from .models import *
from miscellenous.models import *
from datetime import time

# Helper functions and Variables
User = get_user_model()
def staff_required(login_url=None):
    return user_passes_test(lambda u: u.is_staff, login_url=login_url)


# VIEWS
def view_home(request):
    recipes = Recipe.objects.filter(approved=True).order_by('?')[:10]
    context = {'recipes': recipes}
    return render(request, "recipes/index.html", context)


# Login required decorator used so only authenticated users can get
# access to this endpoint
@login_required
def view_create_recipe(request):
    if request.method == 'POST':
        form = request.POST
        images = request.FILES.getlist('images')

        ingredients_quantity = form.getlist('ingredients-quantity')
        ingredients_name = form.getlist('ingredients-name')
        ingredients_unit = form.getlist('ingredients-unit')
        utensils_quantity = form.getlist('utensils-quantity')
        utensils_name = form.getlist('utensils-name')

        category_name = form.get('category')

        print(ingredients_quantity)
        print(ingredients_name)
        print(utensils_quantity)
        print(utensils_name)

        cost = form.get('cost')
        difficulty = form.get('difficulty')
        print(cost)
        print(difficulty)
        
        # Write corresponding character into database
        # v for Very Easy, e for easy and so on
        for diff in DIFFICULTY_CHOICES:
            if diff[1] == difficulty:
                difficulty = diff[0]


        # Write corresponding character into database
        # c for Cheap, m for medium and so on
        for cost_choice in COST_CHOICES:
            if cost_choice[1] == cost:
                cost = cost_choice[0]

        category = Category.objects.get(name=category_name)
        
        # Create a recipe object with form data
        recipe = Recipe(title=form.get('title'), description=form.get('description'),

                        cost=cost, difficulty=difficulty, category=category,

                        preparation_time=time(hour=int(form.get('prep-hours')),
                                            minute=int(form.get('prep-minutes'))),
                        cooking_time=time(hour=int(form.get('cooking-hours')),
                                            minute=int(form.get('cooking-minutes'))),
                        rest_time = time(hour=int(form.get('rest-hours')),
                                            minute=int(form.get('rest-minutes'))),

                        num_of_dishes=form.get('dishes'), 
                        video_url=form.get('youtube-url'),
                        )
        recipe.save()

        print("ingredients: ", ingredients_name)
        print("ingredients: ", ingredients_quantity)
        print("ingredients: ", ingredients_unit)

        # Add images to the recipe
        for image in images:
            RecipeImage(image=image, recipe=recipe).save()

        for ingredient_name, ingredient_unit, ingredient_quantity in zip(ingredients_name, ingredients_unit, ingredients_quantity):
            # Create a IngredientItem object and save it to the database
            print(ingredient_name)
            print(ingredient_quantity)
            print(ingredient_unit)
            ingredient = Ingredient.objects.get(name=ingredient_name)
            IngredientItem(ingredient=ingredient, quantity=ingredient_quantity,
                            unit=ingredient_unit, recipe=recipe).save()

        for utensil_name, utensil_quantity in zip(utensils_name, utensils_quantity):
            # Create a UtensilItem object and save it to the database
            print(utensil_name)
            print(utensil_quantity)
            utensil = Utensil.objects.get(name=utensil_name)
            UtensilItem(utensil=utensil, quantity=utensil_quantity,
                                            recipe=recipe).save()

        # Redirect the user to the detail page of the recipe just created
        return redirect('recipe-detail', recipe.slug)
    
    # Retrieve all ingredients, utensils and categories to
    # show as a choice field in the html template
    ingredients = Ingredient.objects.all()
    utensils = Utensil.objects.all()
    categories = Category.objects.all()
    units = [unit_name for unit, unit_name in UNITS]
    # Create a context dictionary and pass it to the template
    context = {'ingredients': ingredients, 'utensils': utensils,
                'categories': categories, 'units': units}
                
    return render(request, "recipes/add_recipe.html", context=context)


# Login required decorator used so only authenticated users can get
# access to this endpoint
@login_required
def view_create_ingredient(request):
    if request.method == "POST":
        form = request.POST
        # Create a new ingredient
        Ingredient(name = form.get('name'),
                   image = request.FILES.get('image')).save()
        
    return render(request, "recipes/add_ingredients.html")


# Login required decorator used so only authenticated users can get
# access to this endpoint
@login_required
def view_create_utensil(request):
    if request.method == "POST":
        form = request.POST
        print(form)
        # Create a new ingredient
        Utensil(name = form.get('name'),
                image = request.FILES.get('image')).save()
        
        return redirect('home')
        
    return render(request, "recipes/add_utensils.html")


# Use slug as a unique identifier of a recipe in the website
def view_recipe_detail(request, slug):
    recipe = Recipe.objects.get(slug=slug)
    if request.method == "POST":
        # A review was left because http request method is POST
        form = request.POST
        user = request.user
        if isinstance(user, User):
            # Same user can't give more than 1 reviews to a single recipe
            reviews = Review.objects.filter(owner=user)
            if reviews:
                messages.add_message(request, level=messages.WARNING,
                message="Oops! It looks like you have \
                        already given a review to this recipe.\
                        You can't give more than exactly 1 review.")
            else:
                Review(recipe=recipe, rating=form.get('rating'),
                        content=form.get('content'), owner=user).save()
            return redirect('recipe-detail', slug)
        else:
            return redirect('account_login')
    # Get all ingredientItems and utensilItems related the current
    # recipe, Create a context and pass it to the template
    ingredients = recipe.ingredients.all()
    utensils = recipe.utensils.all()
    reviews = recipe.reviews.all()
    # Create a range object/iterator to help render exactly 
    # the number of stars as rating as recipe.average_rating 
    rating_count = range(int(recipe.average_rating))
    images = recipe.recipe_images.all()
    images_length_iterator = range(len(images))
    context = {'recipe': recipe, 'ingredientItems': ingredients, 
                'utensilItems': utensils, 'comments': reviews,
                'rating_count': rating_count, 'images': images,
                'images_length_iterator': images_length_iterator} 
    return render(request, "recipes/recipe_detail.html", context=context)


# API view created for +, - functionality in Recipe detail page
# Takes the slug of the recipe and number of dishes and returns
# a list of ingredient quantities for that particular number of dishes
def get_ingredients_quantity_api_view(request, slug, current_num_of_dishes):
    recipe = Recipe.objects.get(slug=slug)
    print(current_num_of_dishes)
    quantities = recipe.get_quantity_of_ingredients_from_number_of_dishes(current_num_of_dishes)
    return JsonResponse(quantities, safe=False)


# View for category page
def view_category(request):
    categories = Category.objects.all()
    context = {'categories': categories}
    return render(request, 'recipes/category.html', context=context)


# View for category detail page
def view_category_detail(request, slug):
    category = Category.objects.get(slug=slug)
    context = {'category': category}
    return render(request, 'recipes/category_detail.html', context=context)


# Only authenticated users who are also staff members can access to this page
# This is an admin page where staff members can approve a recipe
@login_required
@staff_required(login_url=settings.LOGIN_URL)
def view_non_approved_recipes(request):
    un_approved_recipes = Recipe.objects.filter(approved=False)
    context = {'recipes': un_approved_recipes}
    return render(request, 'recipes/unapproved_recipes.html', context=context)


@login_required
@staff_required(login_url=settings.LOGIN_URL)
def view_non_approved_recipes_detail(request, slug):
    un_approved_recipe = Recipe.objects.get(slug=slug)
    if request.method == "POST":
        # Approve it
        un_approved_recipe.approved = True
        un_approved_recipe.save()
        return redirect('unapproved-recipes')
    context = {'recipe': un_approved_recipe}
    return render(request, 'recipes/unapproved_recipes_detail.html', context=context)
