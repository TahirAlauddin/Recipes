# Generated by Django 3.2.7 on 2022-04-22 08:02

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('miscellenous', '0002_auto_20220422_1302'),
    ]

    operations = [
        migrations.RenameField(
            model_name='review',
            old_name='reviewed_recipe',
            new_name='recipe',
        ),
    ]
