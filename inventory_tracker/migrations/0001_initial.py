# Generated by Django 4.0 on 2022-01-04 14:43

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='IngredientInventory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ingredient_name', models.CharField(max_length=20, verbose_name='Name')),
                ('ingredient_quantity', models.FloatField(help_text='Quantity of the ingredient in the specified unit', verbose_name='Quantity')),
                ('ingredient_unit', models.CharField(help_text='Unit of measurement for the ingredient, such as grams or tbsp', max_length=20, verbose_name='Unit')),
                ('ingredient_price_per_unit', models.FloatField(verbose_name='Price per Unit')),
            ],
            options={
                'verbose_name': 'Ingredient',
                'ordering': ['ingredient_name'],
            },
        ),
        migrations.CreateModel(
            name='MenuItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('menu_item_name', models.CharField(max_length=30, verbose_name='Item Name')),
                ('menu_item_desc', models.CharField(max_length=500, verbose_name='Item Description')),
                ('menu_item_price', models.FloatField(verbose_name='Item Price')),
            ],
            options={
                'verbose_name': 'Menu',
                'ordering': ['menu_item_name'],
            },
        ),
        migrations.CreateModel(
            name='RecipeRequirement',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ingredient_quantity_required', models.FloatField()),
                ('ingredient', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='inventory_tracker.ingredientinventory', verbose_name='Ingredient')),
                ('menu_item_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='inventory_tracker.menuitem', verbose_name='Menu Item')),
            ],
            options={
                'verbose_name': 'Recipe',
                'ordering': ['menu_item_id'],
            },
        ),
        migrations.CreateModel(
            name='PurchaseLog',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('purchase_timestamp', models.DateTimeField(default=django.utils.timezone.now)),
                ('menu_item_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='inventory_tracker.menuitem')),
            ],
        ),
    ]
