from django.shortcuts import render


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

        ingredients_quantity = form.getlist('ingredients-quantity')
        ingredients_name = form.getlist('ingredients-name')
        utensils_quantity = form.getlist('utensils-quantity')
        utensils_name = form.getlist('utensils-name')

        for image in images:
            pass

        for ingredient_quantity in ingredients_quantity:
            pass

        for ingredient_name in ingredients_name:
            pass

        for utensil_name in utensils_name:
            pass

        for utensil_quantity in utensils_quantity:
            pass

        pass

    return render(request, "recipes/create_recipe.html")

