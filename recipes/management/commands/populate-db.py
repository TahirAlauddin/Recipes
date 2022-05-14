from django.core.management.base import BaseCommand
from django.db.utils import IntegrityError
from django.utils.text import slugify
from django.conf import settings

from pickle import load
from recipes.models import *
import os


class Command(BaseCommand):
    help = 'Populate data from pickle files to database'

    def handle(self, *args, **options):

        default_utensil_image = open(os.path.join(settings.MEDIA_ROOT, 'default_utensil.jpg'), 'rb').read()
        default_ingredient_image = open(os.path.join(settings.MEDIA_ROOT, 'default_ingredient.jpg'), 'rb').read()
                
        recipes = load(open("pickle/recipes.pkl", 'rb'))
        utensils = load(open("pickle/utensils.pkl", 'rb'))
        ingredients = load(open("pickle/ingredients.pkl", 'rb'))
        # Hardcoding categories because these are all the categories
        # available in #marmiton
        categories = ["Apéritifs", "Entrées", "Plats", "Desserts", 
                    "Boissons", "Petit-déj/brunch"]
        
        def save_ingredient(name):
            ingredient = Ingredient(name=name)
            ingredient.save()
            ingredient.save_image()

        def save_utensil(name):
            utensil = Utensil(name=name)
            utensil.save()
            utensil.save_image()

        print("Populating ingredients") 
        for name, image in ingredients.items():
            try:
                image_filename = slugify(name) 
                if len(image_filename) > 100:
                    image_filename = image_filename[:100]
                image_filename += '.jpg'
                image_path = os.path.join(settings.MEDIA_ROOT, "ingredients",
                                       image_filename)

                #? Save ingredient image in media_root the directory named ingredients
                with open(image_path, 'wb') as file:
                    if image:
                        file.write(image)
                    else:
                        file.write(default_ingredient_image)

                #? Pass the name of ingredient and path of its image
                save_ingredient(name)

            except IntegrityError:
                print(f"{name} Ingredient already exists in the database")

        
        print("Populating utensils") 
        for name, image in utensils.items():
            try:
                image_filename = slugify(name) 
                if len(image_filename) > 100:
                    image_filename = image_filename[:100]
                image_filename += '.jpg'
                image_path = os.path.join(settings.MEDIA_ROOT, "utensils",
                                          image_filename)

                #? Save utensil image in media_root the directory named utensils
                with open(image_path, 'wb') as file:
                    if image:
                        file.write(image)
                    else:
                        file.write(default_utensil_image)

                #? Pass the name of utensil and path of its image
                save_utensil(name)

            except IntegrityError:
                print(f"{name} Utensil already exists in the database")


        print("Ingredients populated successfully")
        print("Utensils populated successfully")

        if not os.path.exists('media/recipe_images'):
            os.mkdir('media/recipe_images')
        
        for recipe in recipes:
            recipe_obj = Recipe(title=recipe.title, description=recipe.description,
                        cost=recipe.cost, difficulty=recipe.difficulty,
                        preparation_time=recipe.prep_time, cooking_time=recipe.cook_time,
                        rest_time=recipe.rest_time, num_of_dishes=int(recipe.num_of_dishes))

            recipe_obj.save(ingr=recipe.ingredients, utns=recipe.utensils,
                            rcp=recipe)

            print(f"{recipe_obj} saved")
        
        
        for category in categories:
            try:
                Category(name=category).save()

                print(f"{category} saved")
            except IntegrityError:
                print(f"Category {category} already exists in the database.")


        self.stdout.write(self.style.SUCCESS("Database populated successfully."))
