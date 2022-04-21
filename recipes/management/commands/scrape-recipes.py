from django.core.management.base import BaseCommand, CommandError
import requests
from requests.exceptions import ConnectionError
from bs4 import BeautifulSoup
from threading import Thread
from dataclasses import dataclass
from typing import List
from pickle import load, dump
import os

url = 'https://marmiton.org'
DEEPNESS = 4
SAVE_TO_PICKEL = False
PRINT_RESULTS = False

titles = []
threads = []
urls = []
utensil_names = []
ingredients_name_and_units = []
ingredients_names = []

# Database
ingredient_objects = []
utensil_objects = []
recipes_list = []


@dataclass
class Ingredient:
    name: str
    unit: str
    quantity: str
    

@dataclass
class Utensil:
    name: str
    quantity: str
    

@dataclass
class Recipe:
    title: str
    time: str
    difficulty: str
    cost: str
    description: str
    ingredients: List[Ingredient]
    utensils: List[Utensil]


def recursive_parser(response, deepness):
    if deepness >= DEEPNESS:
        return
    soup = BeautifulSoup(response.text, features='lxml')
    time,difficulty,cost = soup.findAll('p', attrs={'class': "RCP__sc-1qnswg8-1 iDYkZP"})

    description_and_steps = soup.find('ul', attrs={'class': None, 'id': None}).getText()
    time = time.getText()
    difficulty = difficulty.getText()
    cost = cost.getText()
    title_recipe = soup.find('title').getText()

    # Recipe with same title already scrapped
    if title_recipe in titles:
        return


    try:
        ingredients_for_recipes = soup.findAll('span', attrs={"class": "SHRD__sc-10plygc-0 epviYI"})
        

        ingredients_name_soup = soup.findAll('span', attrs={'class': "SHRD__sc-10plygc-0 kWuxfa"})
        
        utensils_soup = soup.findAll('div', attrs={"class": "RCP__sc-1641h7i-2 jUeCVL"})

    except AttributeError:
        return

    recipe_utensil_names = []
    recipe_ingredient_names = []


    # Adding utensils to the database if not exists
    for utensil in utensils_soup:
        # Utensils names 
        utensil_text = utensil.getText(strip=True).strip()
        utensil_name = "".join([chr for chr in utensil_text if chr.isalpha()])
        quantity = "".join([chr for chr in utensil_text if chr.isdigit()])
        # utensil_name = utensil_name.replace('\n', ' ')
        # utensil_name = utensil_name.replace('  ', ' ')

        recipe_utensil_names.append(utensil_name)
        if utensil_name not in utensil_names:
            utensil_object = Utensil(name=utensil_name, quantity=quantity)
            utensil_objects.append(utensil_object)
            utensil_names.append(utensil_name)


    # Adding ingredients to database if not exists
    for ingredient_name, ingredient_quantity_and_unit in zip(ingredients_name_soup,
                                                         ingredients_for_recipes):
        ingredient_name = ingredient_name.getText(strip=True).strip()
        qty_unit_text = ingredient_quantity_and_unit.getText(strip=True).strip()

        quantity = ''.join([chr for chr in qty_unit_text if not chr.isalpha()])
        unit = ''.join([chr for chr in qty_unit_text if chr.isalpha()])

        recipe_ingredient_names.append(ingredient_name)
        if ingredient_name not in ingredients_names:
            ingredient_object = Ingredient(name=ingredient_name, unit=unit, quantity=quantity)
            ingredient_objects.append(ingredient_object)


    recipe_ingredients = []
    recipe_utensils = []

    for ingredient_object in ingredient_objects:
        if ingredient_object.name in recipe_ingredient_names:
            recipe_ingredients.append(ingredient_object)


    for utensil_object in utensil_objects:
        if utensil_object.name in recipe_utensil_names:
            recipe_utensils.append(utensil_object)


    # Adding recipe to the database
    recipe = Recipe(title=title_recipe, time=time, difficulty=difficulty,
                    cost=cost, description=description_and_steps, 
                    ingredients=recipe_ingredients, utensils=recipe_utensils)

    recipes_list.append(recipe)
    titles.append(title_recipe)
    
    print("A Recipe added")

    recipes = soup.find('ul', attrs={"class": "RCP__sc-1cs7kbv-3 eTPIie"})


    for recipe in recipes.findChildren('a'):
        try:
            href = recipe['href']

            if not href.startswith('http'):
                href = 'https://marmiton.org' + href 
            
            # Recipe with same Url already scrapped
            if href in urls:
                return

            urls.append(href)
            try:
                response = requests.get(href)
            except ConnectionError:
                print("No Response from", href)
                return
            thread = Thread(target=recursive_parser, args=(response, deepness+1))
            thread.start()
            threads.append(thread)

        except TypeError:
            pass


def scrape_recipes():
    for i in range(5):
        response = requests.get(url)

        soup = BeautifulSoup(response.text, features='lxml')

        recipes = soup.findAll('div', attrs={"class":"m_contenu_bloc"})

        for recipe in recipes:
            result = recipe.findParent('a')
            try:
                href = result['href']
                if href.endswith('html'):
                    continue

                if not href.startswith('http'):
                    href = url + href 

                response = requests.get(href)
                thread = Thread(target=recursive_parser, args=(response, 1))
                thread.start()
                threads.append(thread)

            except TypeError:
                pass


    for thread in threads:
        thread.join()


class Command(BaseCommand):
    help = 'Scrapes recipe data from marmiton.org'

    def handle(self, *args, **options):
        
        scrape_recipes()
        ingredients = []
        utensils = []

        for i in ingredient_objects:
            name = i.name
            if name not in ingredients:
                ingredients.append(name)

        for i in utensil_objects:
            name = i.name
            if name not in utensils:
                utensils.append(name)

        if not os.path.exists('pickle'):
            os.mkdir('pickle')
        dump(recipes_list, open("pickle/recipes.pkl", 'wb'))
        dump(ingredients, open("pickle/ingredients.pkl", 'wb'))
        dump(utensils, open("pickle/utensils.pkl", 'wb'))
        # dump(utensil_objects, open("pickle/utensilsItems.pkl", 'wb'))
        # dump(ingredient_objects, open("pickle/ingredientsItems.pkl", 'wb'))

        self.stdout.write(self.style.SUCCESS("Recipes scrapped successfully."))
