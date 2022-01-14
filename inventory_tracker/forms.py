from django import forms
from .models import MenuItem, RecipeRequirement, IngredientInventory, PurchaseLog
from django.forms import modelformset_factory
from django.core.exceptions import ValidationError

class MenuForm(forms.ModelForm):
    class Meta:
        model = MenuItem
        fields = "__all__"

class RecipeForm(forms.ModelForm):
    class Meta:
        model = RecipeRequirement
        fields = "__all__"

class InventoryForm(forms.ModelForm):
    class Meta:
        model = IngredientInventory
        fields = "__all__"

class PurchaseForm(forms.ModelForm):
    class Meta:
        model = PurchaseLog
        fields = "__all__"
    def clean_menu_item_id(self):
        menu_item = self.cleaned_data['menu_item_id']
        ingredients_list = RecipeRequirement.objects.filter(menu_item_id = menu_item)
        if not ingredients_list:
            raise ValidationError(f"No recipe found for {menu_item}!") 
        for ingredient in ingredients_list:
                qty_required = ingredient.ingredient_quantity_required
                inventory_obj = IngredientInventory.objects.get(ingredient_name = ingredient.ingredient)
                if not inventory_obj:
                    raise ValidationError(f"No {ingredient} in the inventory!") 
                current_qty = inventory_obj.ingredient_quantity
                if current_qty < qty_required:
                    raise ValidationError(f"Not enough {ingredient} in the inventory!")
        return menu_item


RecipeFormSet = modelformset_factory(RecipeRequirement, fields=['menu_item_id', 'ingredient', 'ingredient_quantity_required'], max_num = 20)
