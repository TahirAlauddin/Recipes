# Generated by Django 3.2.7 on 2022-04-24 14:57

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0018_recipe_youtube_link'),
    ]

    operations = [
        migrations.RenameField(
            model_name='recipe',
            old_name='youtube_link',
            new_name='video_url',
        ),
    ]