# Generated by Django 3.2.7 on 2022-04-24 07:53

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('miscellenous', '0004_category_image'),
    ]

    operations = [
        migrations.RenameField(
            model_name='review',
            old_name='user',
            new_name='owner',
        ),
    ]