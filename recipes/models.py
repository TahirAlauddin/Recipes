from django.db import models
from django.utils.translation import gettext_lazy as _
from django.utils.text import slugify
from miscellenous.models import Category
from django.db.utils import IntegrityError
from datetime import time, timedelta

UNITS = [
    # Volume
    ("tsp", "teaspoon"),
    ("tbsp", "tablespoon"),
    ("c", "cup"),
    ("pt", "pint"),
    ("qt", "quart"),
    ("gal", "gallon"),
    ("ml", "milliliter"), 
    ("l", "liter"), 
    ("dl", "deciliter"),
    ("fl oz", "fluid ounce"),

    # Mass and Weight
    ("lb", "pound"),
    ("oz", "ounce"),
    ("mg", "milligram"),
    ("g", "gram"),
    ("kg", "kilogram"),

    # Length
    ("mm", "millimeter"),
    ("cm", "centimeter"),
    ("m", "meter"),
    ("in", "inch"),
]


DIFFICULTY_CHOICES = [
    ('v', 'Very Easy'),
    ('e', 'Easy'),
    ('m', 'Medium'),
    ('h', 'Hard'),
]

COST_CHOICES =  [
    ('l', 'Low'),
    ('m', 'Medium'),
    ('h', 'High'),
]


class RecipeImage(models.Model):
    """"
    A Photo/Picture of a recipe
    There is a One to Many Relationship between Recipe and
    RecipeImage. Hence, there can be many images belonging 
    to a single Recipe.
    - image: The actual image or path to the image on server
    - recipe: The Recipe the image belongs to

    """
    image = models.ImageField(upload_to='images')
    recipe = models.ForeignKey("Recipe", related_name='recipe_images',
                                on_delete=models.CASCADE, null=True)

    def __str__(self):
        """ String Representation of the object of RecipeImage """
        return str(self.recipe) + " " + str(self.pk)
    
    
    class Meta:
        """ Meta Configurations of the class RecipeImage """
        verbose_name = _('Recipe Image')
        verbose_name_plural = _('Recipe Images')
        ordering = ['recipe']


class Ingredient(models.Model):
    """"
    An Ingredient of a product, a recipe in this case.
    There is a Many to Many Relationship between Recipe and
    Ingredient. Hence, there can be many Ingredients belonging 
    to a single Recipe and also many Recipes pointing to same
    Ingredient.
    - name: The name of the Ingredient i.e. Tomato, Water etc.
    - unit: The unit of the Ingredient i.e. Gram (g), Litre (l) etc.
    - approved: Whether the Ingredient is approved or not
    """
    name = models.CharField(max_length=120, 
                            unique=True,
                            help_text="Maximum 120 characters",
                            )
    image = models.ImageField(upload_to='ingredient_items',
                                    default='default_ingredient.jpg')
    approved = models.BooleanField(null=False, default=False)

    # unit = models.ForeignKey(Unit, null=True, blank=True, on_delete=models.PROTECT)
    
    def __str__(self):
        """ String Representation of the object of Ingredient """
        return self.name

    @property
    def name2(self):
        return self.name

    class Meta:
        """ Meta Configurations of the class Ingredient """
        # The order in which ingredients show on admin panel
        ordering = ['name'] 
        # The name which shows on the admin page
        verbose_name = _('Ingredient')
        # The plural name which shows on the admin page
        verbose_name_plural = _('Ingredients')


class Utensil(models.Model):
    """"
    A utensil which is need to cook/make/bake a recipe or a product.
    There is a Many to Many Relationship between Recipe and
    Utensil. Hence, there can be many Utensils belonging 
    to a single Recipe and also many Recipes pointing to same
    Utensil.
    - name: The name of the Utensil i.e. Plates, Spoon etc.
    """
    name = models.CharField(max_length=120, 
                            unique=True,
                            help_text="Maximum 120 characters",
                            )
    image = models.ImageField(upload_to='utensil_items',
                                default='default_utensil.jpg')

    def __str__(self):
        """ String Representation of the object of Utensil """
        return self.name

    class Meta:
        """ Meta Configurations of the class Utensil """
        # The order in which Utensils show on admin panel
        ordering = ['name']
        # The name which shows on the admin page
        verbose_name = _('Utensil')
        # The plural name which shows on the admin page
        verbose_name_plural = _('Utensils')


class IngredientItem(models.Model):
    """"
    It is and IngredientItem which is used for relating Ingredient and Recipe.
        There is One to Many relationship between IngredientItem and Ingredient
        There is One to Many relationship between Ingredient Item and Recipe
    - title: The name of the Ingredient i.e. Milk, Butter etc.
    - quantity: The quantity of the Ingredient 
    - utensil: The Ingredient related to it
    - recipe: The Recipe to which IngredientItem belongs to
    """
    quantity = models.CharField(max_length=10)
    ingredient = models.ForeignKey(to=Ingredient, 
                            on_delete=models.CASCADE)
    unit = models.CharField(max_length=10, #choices=UNITS,
                            help_text="Maximum 50 characters",
                            null=True, blank=True
                            )
    recipe = models.ForeignKey(to="Recipe", 
                            on_delete=models.CASCADE,
                            related_name='ingredients')

    def __str__(self):
        """ String representation of UtensilItem """
        return str(self.ingredient) + f"({self.quantity} {self.unit})"
    

class UtensilItem(models.Model):
    """"
    It is a Utensil item which is used for relating Utensil with Recipe
        There is One to Many relationship between Utensil Item and Utensil
        There is One to Many relationship between Utensil Item and Recipe
    - title: The name of the Utensil i.e. Plates, Spoon etc.
    - quantity: The quantity of the Utensil
    - utensil: The Utensil related to it
    - recipe: The Recipe to which Utensil Item belongs to
    """
    quantity = models.CharField(max_length=10)
    utensil = models.ForeignKey(to=Utensil, 
                            on_delete=models.CASCADE)
    recipe = models.ForeignKey(to="Recipe", 
                            on_delete=models.CASCADE,
                            related_name='utensils')

    def __str__(self):
        """ String representation of UtensilItem """
        if self.quantity == '1':
            return f"{self.quantity} {self.utensil}" 
        # Add an s at the end of it is plural
        return f"{self.quantity} {self.utensil}s" 
        

class Recipe(models.Model):
    """"
    Recipe of a Food which consists of several fields and attributes
    Forexample:
    - title: Unique title of the Recipe i.e. Chinese Rice, Italian Pizza etc.
    - description: Free Text/Description or steps of making a recipe
    - slug: A unique url/slug of the Recipe i.e. chinese-rice-recipe etc.
    - preparation_time: The time it takes to make a recipe i.e. 10 min
    - cooking_time: The time it takes to cook the recipe
    - rest_time: The time it takes after cooking
    - difficulty: How much difficult it is to make the recipe i.e Easy, Medium
    - cost: The cost category which the Recipe belongs to i.e. Low, High 
    - approved: Whether the recipe is approved or not 
    """
    title = models.CharField(unique=True, 
                            max_length=120)
    description = models.TextField(blank=True)
    slug = models.SlugField(unique=True, max_length=120,
                                    null=False, blank=False)
    
    preparation_time = models.TimeField(default=time)
    cooking_time = models.TimeField(default=time)
    rest_time = models.TimeField(default=time)

    difficulty = models.CharField(max_length=1, choices=DIFFICULTY_CHOICES)
    cost = models.CharField(max_length=1, choices=COST_CHOICES)
    category = models.ForeignKey(to=Category, on_delete=models.SET_NULL,
                                null=True)
    approved = models.BooleanField(null=False, default=False)

    def __str__(self):
        """ String representation of the Recipe class"""
        return self.title


    def get_preparation_time(self):
        xt = timedelta(self.preparation_time)
        yt = timedelta(self.cooking_time)
        zt = timedelta(self.rest_time)

        nt = xt + yt + zt

        hours = nt.seconds // 3600
        rest = nt.seconds % 3600
        minutes = rest // 60
        seconds = rest % 60

        full_preparation_time = time(hour=hours, minute=minutes, second=seconds)

        return full_preparation_time


    def save(self, *args, **kwargs):
        """ Overriding save method of models.Model to automatically 
        slugify each recipe using its title """
        ingredients = kwargs.pop('ingr')
        utensils = kwargs.pop('utns')
        try:
            self.slug = slugify(self.title)
            super(Recipe, self).save(*args, **kwargs)

            for ingredient in ingredients:
                ingredientItem = IngredientItem(quantity=ingredient.quantity, unit=ingredient.unit,
                                            ingredient=Ingredient.objects.filter(name=ingredient.name).first(),
                                            recipe=self)
                ingredientItem.save()


            for utensil in utensils:
                utensilItem = UtensilItem(quantity=utensil.quantity, 
                                            utensil=Utensil.objects.get(name=utensil.name),
                                            recipe=self)

        except IntegrityError:
            pass
           

    class Meta:
        ordering = ['title']
        verbose_name = _('Recipe')
        verbose_name_plural = _('Recipes')
