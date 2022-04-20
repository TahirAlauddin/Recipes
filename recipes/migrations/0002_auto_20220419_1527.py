# Generated by Django 3.2.7 on 2022-04-19 10:27

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='recipe',
            name='recipe_images',
        ),
        migrations.AddField(
            model_name='recipeimage',
            name='recipe',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='recipe_images', to='recipes.recipe'),
        ),
    ]