# Generated by Django 3.2.7 on 2022-04-19 10:16

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='Maximum 120 characters', max_length=120, unique=True, verbose_name='Category|name')),
                ('slug', models.SlugField(help_text='Automatically generated from the title', unique=True)),
            ],
            options={
                'verbose_name': 'Category',
                'verbose_name_plural': 'Categories',
            },
        ),
        migrations.CreateModel(
            name='Ingredient',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='Maximum 120 characters', max_length=120, verbose_name='Ingredient|name')),
                ('unit', models.CharField(help_text='Maximum 50 characters', max_length=50, verbose_name='Ingredient|unit')),
            ],
            options={
                'verbose_name': 'Ingredient',
                'verbose_name_plural': 'Ingredients',
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='Recipe',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=120, verbose_name='Recipe|Title')),
                ('description', models.TextField(blank=True, verbose_name='Recipe|Description')),
                ('slug', models.SlugField(max_length=120, unique=True)),
                ('preparation_time', models.CharField(blank=True, max_length=100, verbose_name='Recipe|Preperation Time')),
                ('difficulty', models.CharField(choices=[('e', 'Easy'), ('m', 'Medium'), ('h', 'Hard')], max_length=1, verbose_name='Recipe|Difficulty')),
                ('cost', models.CharField(choices=[('l', 'Low'), ('m', 'Medium'), ('h', 'High')], max_length=1, verbose_name='Recipe|Cost')),
                ('category', models.ManyToManyField(to='recipes.Category', verbose_name='Recipe|Category')),
            ],
            options={
                'verbose_name': 'Recipe',
                'verbose_name_plural': 'Recipes',
                'ordering': ['title'],
            },
        ),
        migrations.CreateModel(
            name='RecipeImage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='images')),
            ],
            options={
                'verbose_name': 'Recipe Image',
                'verbose_name_plural': 'Recipe Images',
            },
        ),
        migrations.CreateModel(
            name='Utensil',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='Maximum 120 characters', max_length=120, verbose_name='Utensil|name')),
            ],
            options={
                'verbose_name': 'Utensil',
                'verbose_name_plural': 'Utensils',
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='UtensilItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.FloatField()),
                ('recipe', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='utensils', to='recipes.recipe')),
                ('utensil', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='recipes.utensil')),
            ],
        ),
        migrations.AddField(
            model_name='recipe',
            name='recipe_images',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='recipe', to='recipes.recipeimage'),
        ),
        migrations.CreateModel(
            name='IngredientItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.FloatField()),
                ('ingredient', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='recipes.ingredient')),
                ('recipe', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='ingredients', to='recipes.recipe')),
            ],
        ),
    ]