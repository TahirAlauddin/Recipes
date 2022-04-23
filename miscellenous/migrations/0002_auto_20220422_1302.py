# Generated by Django 3.2.7 on 2022-04-22 08:02

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0014_auto_20220422_1153'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('miscellenous', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='review',
            name='reviewed_recipe',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reviews', to='recipes.recipe'),
        ),
        migrations.AlterField(
            model_name='review',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL),
        ),
    ]
