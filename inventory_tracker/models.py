from django.db import models
from django.utils.timezone import now
from django.urls import reverse

# Create your models here.
class MenuItem(models.Model):
    menu_item_name = models.CharField(max_length=30, verbose_name = "Item Name")
    menu_item_desc = models.CharField(max_length=500, verbose_name = "Item Description")
    menu_item_price = models.FloatField(verbose_name = "Item Price")
    menu_category = models.ForeignKey('MenuItemCategory', on_delete=models.CASCADE, verbose_name = "Item Category")
    def get_absolute_url(self):
        return reverse("menu_detail", kwargs={'pk': self.pk})

    def get_recipe_url(self):
        return reverse("recipe_detail", kwargs={'pk': self.pk})

    class Meta:
        ordering = ["menu_item_name"]
        verbose_name = "Menu"

    def __str__(self):
        return self.menu_item_name

class MenuItemCategory(models.Model):
    category = models.CharField(max_length = 30)

    def __str__(self):
        return str(self.category)

class RecipeRequirement(models.Model):
    menu_item_id = models.ForeignKey('MenuItem', on_delete=models.CASCADE, verbose_name = "Menu Item")
    ingredient = models.ForeignKey('IngredientInventory', on_delete=models.CASCADE, verbose_name = "Ingredient")
    ingredient_quantity_required = models.FloatField()

    class Meta:
        ordering = ["menu_item_id"]
        verbose_name = "Recipe"

    def __str__(self):
        return str(self.ingredient) + " for " + str(self.menu_item_id)
    
    def get_absolute_url(self):
        return reverse('recipe_detail', kwargs={'pk': self.pk})

class IngredientInventory(models.Model):
    ingredient_name = models.CharField(max_length=20, verbose_name = "Name")
    ingredient_quantity = models.FloatField(verbose_name = "Quantity", help_text= "Quantity of the ingredient in the specified unit")
    ingredient_unit = models.CharField(max_length=20, verbose_name = "Unit", help_text="Unit of measurement for the ingredient, such as grams or tbsp")
    ingredient_price_per_unit = models.FloatField(verbose_name = "Price per Unit")

    def __str__(self):
        return self.ingredient_name
    
    class Meta:
        ordering = ["ingredient_name"]
        verbose_name = "Ingredient"
    
    def get_absolute_url(self):
        return "/inventory"

class PurchaseLog(models.Model):
    purchase_timestamp = models.DateTimeField(default=now)
    menu_item_id = models.ForeignKey('MenuItem', on_delete=models.CASCADE)

    def get_absolute_url(self):
        return "/purchase_log"

    def __str__(self):
        return str(self.purchase_timestamp) + " Purchase"