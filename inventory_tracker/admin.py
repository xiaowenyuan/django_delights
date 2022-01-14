from django.contrib import admin

# Register your models here.
from .models import MenuItem, RecipeRequirement, IngredientInventory, PurchaseLog, MenuItemCategory

admin.site.register(MenuItem)
admin.site.register(RecipeRequirement)
admin.site.register(IngredientInventory)
admin.site.register(PurchaseLog)
admin.site.register(MenuItemCategory)