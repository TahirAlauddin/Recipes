from django.core.management.base import BaseCommand, CommandError
from pickle import load
from recipes.models import *

class Command(BaseCommand):
    help = 'Populate data from pickle files to database'

    def handle(self, *args, **options):
        
        recipes = load(open("pickle/recipes.pkl", 'rb'))
        utensils = load(open("pickle/utensils.pkl", 'rb'))
        ingredients = load(open("pickle/ingredients.pkl", 'rb'))
        
        print("Populating ingredients") 
        ingredient_objects = [Ingredient(name=ingredient) for ingredient in ingredients]
        Ingredient.objects.bulk_create(ingredient_objects)
        print("Ingredients populated successfully")

        print("Populating utensils") 
        utensil_objects = [Utensil(name=utensil) for utensil in utensils]
        Utensil.objects.bulk_create(utensil_objects)
        print("Utensils populated successfully")
        
        for recipe in recipes:
            recipe_obj = Recipe(title=recipe.title, description=recipe.description,
                        cost=recipe.cost, difficulty=recipe.difficulty,
                        preparation_time=recipe.prep_time, cooking_time=recipe.cook_time,
                        rest_time=recipe.rest_time)

            recipe_obj.save(ingr=recipe.ingredients, utns=recipe.utensils)

            print(f"{recipe_obj} saved")


        self.stdout.write(self.style.SUCCESS("Database populated successfully."))
