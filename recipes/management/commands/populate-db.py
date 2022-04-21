from django.core.management.base import BaseCommand, CommandError
from pickle import load
from recipes.models import *

class Command(BaseCommand):
    help = 'Populate data from pickle files to database'

    def handle(self, *args, **options):
        
        recipes = load(open("pickle/recipes.pkl", 'rb'))
        utensils = load(open("pickle/utensils.pkl", 'rb'))
        ingredients = load(open("pickle/ingredients.pkl", 'rb'))
        
        """Commented out because already saved to database, it will cause integrity error"""
        # for ingredient in ingredients:
        #     ingredient = Ingredient(name=ingredient)
        #     ingredient.save()

        # for utensil in utensils:
        #     utensil = Utensil(name=utensil)
        #     utensil.save()

        for recipe in recipes:
            recipe_obj = Recipe(title=recipe.title, description=recipe.description,
                        cost=recipe.cost, difficulty=recipe.difficulty,
                        preparation_time=recipe.time)

            recipe_obj.save()

            for ingredient in recipe.ingredients:
                ingredientItem = IngredientItem(quantity=ingredient.quantity, unit=ingredient.unit,
                                            ingredient=Ingredient.objects.get(name=ingredient.name),
                                            recipe=recipe_obj)
                ingredientItem.save()


            for utensil in recipe.utensils:
                utensilItem = UtensilItem(quantity=utensil.quantity, 
                                            utensil=Utensil.objects.get(name=utensil.name),
                                            recipe=recipe_obj)

                utensilItem.save()


        self.stdout.write(self.style.SUCCESS("Database populated successfully."))
