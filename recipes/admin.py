from django.contrib import admin
from .models import *


class UtensilAdmin(admin.ModelAdmin):
    model = Utensil
    list_display = ('name',)
    search_fields = ('name',)

class IngredientAdmin(admin.ModelAdmin):
    model = Ingredient
    list_display = ('name', 'approved')
    search_fields = ('name',)

class RecipeAdmin(admin.ModelAdmin):
    list_display = ('title', 'approved', 'cost', 'difficulty', 'prep_time',)
    list_filter = ('category', 'cost', 'difficulty',)
    search_fields = ('title', 'category__name',)
    prepopulated_fields = {'slug': ('title',)}
    model = Recipe

    @admin.display(empty_value='???')
    def prep_time(self, obj):
        time = f"{obj.preparation_time.minute} minutes"
        if obj.preparation_time.hour:
            time = f"{obj.preparation_time.hour} hours" + time
        return time


admin.site.register(Recipe, RecipeAdmin)
admin.site.register(Ingredient, IngredientAdmin)
admin.site.register(Utensil, UtensilAdmin)
admin.site.register(RecipeImage)
admin.site.register(IngredientItem)
admin.site.register(UtensilItem)
