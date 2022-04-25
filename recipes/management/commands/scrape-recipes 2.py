from django.core.management.base import BaseCommand, CommandError
import requests
from requests.exceptions import ConnectionError
from bs4 import BeautifulSoup
from threading import Thread
from dataclasses import dataclass
from typing import List, Any
from pickle import load, dump
import os
from datetime import time

url = 'https://marmiton.org'
DEEPNESS = 50
SAVE_TO_PICKEL = True
PRINT_RESULTS = False
RECURSIVE = True
RANDOM = True

skipped = 0
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
    prep_time: Any
    rest_time: Any
    cook_time: Any
    difficulty: str
    cost: str
    description: str
    ingredients: List[Ingredient]
    utensils: List[Utensil]


def str_to_time(prep_time, rest_time, cook_time):

    prep_time = prep_time.getText()
    rest_time = rest_time.getText()
    cook_time = cook_time.getText()

    if prep_time == '-':
        prep_time = time()
    else:
        prep_time_list = prep_time.split()
        num = prep_time_list[::2]
        unit = prep_time_list[1::2]

        minute = 0
        hour = 0
        for u, n in zip(unit, num):
            if u == 'hour':
                hour = n
            elif u == 'min':
                minute = n

        prep_time = time(hour=int(hour), minute=int(minute))
    
    if cook_time == '-':
        cook_time = time()
    else:
        cook_time_list = cook_time.split()
        num = cook_time_list[::2]
        unit = cook_time_list[1::2]

        minute = 0
        hour = 0
        for u, n in zip(unit, num):
            if u == 'hour':
                hour = n
            elif u == 'min':
                minute = n

        cook_time = time(hour=int(hour), minute=int(minute))

    if rest_time == '-':
        rest_time = time()
    else:
        rest_time_list = rest_time.split()
        num = rest_time_list[::2]
        unit = rest_time_list[1::2]

        minute = 0
        hour = 0
        for u, n in zip(unit, num):
            if u == 'hour':
                hour = n
            elif u == 'min':
                minute = n

        rest_time = time(hour=int(hour), minute=int(minute))
        
    return prep_time, rest_time, cook_time


def recursive_parser(response, deepness):
    global skipped
    if deepness >= DEEPNESS:
        return
    soup = BeautifulSoup(response.text, features='lxml')
    _,difficulty,cost = soup.findAll('p', attrs={'class': "RCP__sc-1qnswg8-1 iDYkZP"})

    description_and_steps = soup.find('ul', attrs={'class': None, 'id': None}).getText()

    times = soup.findAll('span', attrs={'class': "SHRD__sc-10plygc-0 bzAHrL"})

    prep_time, rest_time, cook_time = times[1:]


    # converting string time to time object python
    prep_time, rest_time, cook_time = str_to_time(prep_time, rest_time, cook_time)

    difficulty = difficulty.getText()
    cost = cost.getText()
    title_recipe = soup.find('title').getText()

    # Recipe with same title already scrapped
    if title_recipe in titles:
        skipped += 1
        return

    try:
        ingredients_for_recipes = soup.findAll('span', attrs={"class": "SHRD__sc-10plygc-0 epviYI"})

        ingredients_name_soup = soup.findAll('span', attrs={'class': "SHRD__sc-10plygc-0 kWuxfa"})
        
        utensils_soup = soup.findAll('div', attrs={"class": "RCP__sc-1641h7i-2 jUeCVL"})

    except AttributeError:
        return

    recipe_utensil_names = []
    recipe_ingredient_names = []


    # Adding ingredients to database if not exists
    for ingredient_name, ingredient_quantity_and_unit in zip(ingredients_name_soup,
                                                         ingredients_for_recipes):
        ingredient_name = ingredient_name.getText(strip=True).strip()
        qty_unit_text = ingredient_quantity_and_unit.getText(strip=True).strip()

        quantity = ''.join([chr for chr in qty_unit_text if chr.isdigit() or chr == '/'])
        unit = ''.join([chr for chr in qty_unit_text if chr.isalpha()])

        recipe_ingredient_names.append(ingredient_name)

        if len(ingredient_name) > 20:
            skipped += 1
            return

        for i in ingredient_name:
            if i.isdigit():
                skipped += 1
                return

        if ingredient_name not in ingredients_names:
            ingredient_object = Ingredient(name=ingredient_name, unit=unit, quantity=quantity)
            ingredient_objects.append(ingredient_object)
            ingredients_names.append(ingredient_name)


    # Adding utensils to the database if not exists
    for utensil in utensils_soup:
        # Utensils names 
        utensil_text = utensil.getText(strip=True).strip()
        utensil_name = "".join([chr for chr in utensil_text if chr.isalpha()])
        quantity = "".join([chr for chr in utensil_text if chr.isdigit()])

        recipe_utensil_names.append(utensil_name)
        if utensil_name not in utensil_names:
            utensil_object = Utensil(name=utensil_name, quantity=quantity)
            utensil_objects.append(utensil_object)
            utensil_names.append(utensil_name)

    recipe_ingredients = []
    recipe_utensils = []

    for ingredient_object in ingredient_objects:
        if ingredient_object.name in recipe_ingredient_names:
            recipe_ingredients.append(ingredient_object)


    for utensil_object in utensil_objects:
        if utensil_object.name in recipe_utensil_names:
            recipe_utensils.append(utensil_object)


    if difficulty.lower() == "très facile":
        difficulty = 'v'
    elif difficulty.lower() == "facile":
        difficulty = 'e'
    elif difficulty.lower() == "niveau moyen":
        difficulty = 'm'
    elif difficulty.lower() == "difficile":
        difficulty = 'h'

    if cost.lower() == 'bon marché':
        cost = 'l'
    elif cost.lower() == 'coût moyen':
        cost = 'm'
    elif cost.lower() == 'assez cher':
        cost = 'h'

    # Adding recipe to the database
    recipe = Recipe(title=title_recipe, prep_time=prep_time, cook_time=cook_time, 
                    rest_time=rest_time, difficulty=difficulty,
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
    # for i in range(5):
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

