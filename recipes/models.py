from django.db import models
from django.utils.translation import gettext_lazy as _


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
    ('e', 'Easy'),
    ('m', 'Medium'),
    ('h', 'Hard'),
]
COST_CHOICES =  [
    ('l', 'Low'),
    ('m', 'Medium'),
    ('h', 'High'),
]

class Category(models.Model):
    """"
    The Category of a product, in this case the Recipe.
    name
    - name: A unique name/title of a Category
    - slug: A unique Slug/Url of a Category
    """
    name = models.CharField(max_length=120,
                            unique=True,
                            help_text="Maximum 120 characters",
                            verbose_name=_('Category|name'))
    slug = models.SlugField(unique=True, 
                            help_text='Automatically generated from the title')
    
    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _('Category')
        verbose_name_plural = _('Categories')
    

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

    """
    name = models.CharField(max_length=120, 
                            help_text="Maximum 120 characters",
                            verbose_name = _("Ingredient|name"),
                            )
    unit = models.CharField(max_length=10, choices=UNITS,
                            help_text="Maximum 50 characters",
                            verbose_name=_("Ingredient|unit"),
                            )
    # unit = models.ForeignKey(Unit, null=True, blank=True, on_delete=models.PROTECT)
    
    def __str__(self):
        """ String Representation of the object of Ingredient """
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
                            help_text="Maximum 120 characters",
                            verbose_name=_('Utensil|name'),
                            )

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
    image = models.ImageField(upload_to='ingredient_items',
                                    default='default_ingredient.jpg')
    quantity = models.FloatField()
    ingredient = models.OneToOneField(to=Ingredient, 
                            on_delete=models.CASCADE)
    recipe = models.ForeignKey(to="Recipe", 
                            on_delete=models.CASCADE,
                            related_name='ingredients')

    def __str__(self):
        return str(self.ingredient) + f"({self.quantity} {self.ingredient.unit})"
    

class UtensilItem(models.Model):
    image = models.ImageField(upload_to='utensil_items',
                                default='default_utensil.jpg')
    quantity = models.IntegerField()
    utensil = models.OneToOneField(to=Utensil, 
                            on_delete=models.CASCADE)
    recipe = models.ForeignKey(to="Recipe", 
                            on_delete=models.CASCADE,
                            related_name='utensils')

    def __str__(self):
        if self.quantity == 1:
            return f"{self.quantity} {self.utensil}" 
        return f"{self.quantity} {self.utensil}s" 
        

class Recipe(models.Model):
    title = models.CharField(max_length=120, verbose_name=_('Recipe|Title'))
    description = models.TextField(blank=True, 
                                    verbose_name=_('Recipe|Description'))
    slug = models.SlugField(unique=True, max_length=120,
                                    null=False, blank=False)
    preparation_time = models.CharField(max_length=100, blank=True,
                                verbose_name=_('Recipe|Preperation Time')
                                )
    difficulty = models.CharField(max_length=1, 
                                choices=DIFFICULTY_CHOICES,
                                verbose_name=_('Recipe|Difficulty')
                                )
    cost = models.CharField(max_length=1, choices=COST_CHOICES,
                            verbose_name=_('Recipe|Cost')
                            )
    category = models.ManyToManyField(Category,
                                verbose_name=_('Recipe|Category')
                                )


    def __str__(self):
        return self.title

    class Meta:
        ordering = ['title']
        verbose_name = _('Recipe')
        verbose_name_plural = _('Recipes')

