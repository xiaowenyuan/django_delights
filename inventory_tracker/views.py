from django.shortcuts import render, redirect
from django.views.generic import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from .models import MenuItem, RecipeRequirement, IngredientInventory, PurchaseLog
from .forms import MenuForm, RecipeForm, InventoryForm, RecipeFormSet, PurchaseForm
from django.http import HttpResponseRedirect, HttpResponse
from django.db.models import Sum, F
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required

# Create your views here.
@login_required
def home(request):
    #purchased_items = PurchaseLog.objects.select_related('menu_item_id')
    #print(purchased_items.query)
    #print(type(purchased_items))
    purchased_items_price = PurchaseLog.objects.aggregate(Sum('menu_item_id__menu_item_price'))
    ingredients_price = IngredientInventory.objects.aggregate(price_sum = Sum(F('ingredient_quantity') * F('ingredient_price_per_unit')))
    costs = ingredients_price['price_sum']
    income = purchased_items_price['menu_item_id__menu_item_price__sum']
    profit = income - costs
    context = {'costs': costs, 'income': income, 'profit': profit, "name": request.user}
    return render(request, "inventory_tracker/home.html", context)

def login_view(request):
    context = {
    "login_view": "active"
  }
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username = username, password = password)
        if user is not None:
            login(request, user)
            return redirect("home")
        else:
            return HttpResponse("invalid credentials")
    return render(request, "registration/login.html", context)

@login_required
def logout_view(request):
    logout(request)
    return redirect("home")

class SignUp(LoginRequiredMixin,CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy("login")
    template_name = "registration/signup.html"

class MenuList(LoginRequiredMixin,ListView):
    model = MenuItem
    template_name = "inventory_tracker/menu_list.html"
    context_object_name = 'menu_item'

class MenuDetail(LoginRequiredMixin,DetailView):
    model = MenuItem 
    template_name = "inventory_tracker/menu_detail.html"

class MenuItemCreate(LoginRequiredMixin, CreateView):
    model = MenuItem
    template_name = "inventory_tracker/menu_item_create.html"
    form_class = MenuForm

class MenuItemUpdate(LoginRequiredMixin, UpdateView):
    model = MenuItem
    template_name = "inventory_tracker/menu_item_update.html"
    form_class = MenuForm

class MenuItemDelete(LoginRequiredMixin, DeleteView):
    model = MenuItem
    template_name = "inventory_tracker/menu_item_delete.html"
    success_url = "/menu/"

class RecipeList(LoginRequiredMixin, ListView):
    model = MenuItem
    template_name = "inventory_tracker/recipe_list.html"
    context_object_name = 'recipe_item'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['recipe_avail'] = RecipeRequirement.objects.all()
        return context

class RecipeDetail(LoginRequiredMixin, DetailView):
    model = MenuItem
    template_name = "inventory_tracker/recipe_detail.html"
    context_object_name = 'recipe_item'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['recipe_req_list'] = RecipeRequirement.objects.filter(menu_item_id=self.object)
        context['recipe_ingredient_query'] = RecipeRequirement.objects.select_related('ingredient')
        return context

class RecipeCreate(LoginRequiredMixin, CreateView):
    model = RecipeRequirement
    template_name = "inventory_tracker/recipe_create.html"
    form_class = RecipeForm

    def get_context_data(self, **kwargs):
        context = super(RecipeCreate, self).get_context_data(**kwargs)
        context['formset'] = RecipeFormSet(queryset = RecipeRequirement.objects.none())
        return context
    
    def post(self, request, *args, **kwargs):
        formset = RecipeFormSet(request.POST)
        if formset.is_valid():
            return self.form_valid(formset)

    def form_valid(self, formset):
        instances = formset.save(commit = False)
        for instance in instances:
            instance.save()
        return HttpResponseRedirect('/recipe')

class RecipeUpdate(LoginRequiredMixin, UpdateView):
    model = RecipeRequirement
    template_name = "inventory_tracker/recipe_update.html"
    form_class = RecipeForm

class RecipeDelete(LoginRequiredMixin, DeleteView):
    model = RecipeRequirement
    template_name = "inventory_tracker/recipe_delete.html"
    success_url = "/recipe"

class InventoryList(LoginRequiredMixin, ListView):
    model = IngredientInventory
    template_name = "inventory_tracker/inventory_list.html"
    
class InventoryCreate(LoginRequiredMixin, CreateView):
    model = IngredientInventory
    template_name = "inventory_tracker/inventory_create.html"
    form_class = InventoryForm

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            ingredientname = form.cleaned_data['ingredient_name']
            ingredientqty = form.cleaned_data['ingredient_quantity']
            ingredientunit = form.cleaned_data['ingredient_unit']
            ingredientppu = form.cleaned_data['ingredient_price_per_unit']
            toupdate = {'ingredient_name': ingredientname, 'ingredient_quantity': ingredientqty, 'ingredient_unit': ingredientunit, 'ingredient_price_per_unit': ingredientppu}
            IngredientInventory.objects.update_or_create(ingredient_name = ingredientname, defaults = toupdate)
            return HttpResponseRedirect('/inventory')
        return render(request, self.template_name, {'form': form})

class InventoryUpdate(LoginRequiredMixin, UpdateView):
    model = IngredientInventory
    template_name = "inventory_tracker/inventory_update.html"
    form_class = InventoryForm

class InventoryDelete(LoginRequiredMixin, DeleteView):
    model = IngredientInventory
    template_name = "inventory_tracker/inventory_delete.html"
    success_url = "/inventory"

class PurchaseLogList(LoginRequiredMixin, ListView):
    model = PurchaseLog
    template_name = "inventory_tracker/purchase_list.html"

class PurchaseCreate(LoginRequiredMixin, CreateView):
    model = PurchaseLog
    template_name = "inventory_tracker/purchase_create.html"
    form_class = PurchaseForm

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            datestamp = form.cleaned_data['purchase_timestamp']
            menu_item = form.cleaned_data['menu_item_id']
            new_purchase_obj = PurchaseLog()
            new_purchase_obj.menu_item_id = menu_item
            new_purchase_obj.purchase_timestamp = datestamp
            new_purchase_obj.save()
            ingredients_list = RecipeRequirement.objects.filter(menu_item_id = menu_item)
            for ingredient in ingredients_list:
                qty_required = ingredient.ingredient_quantity_required
                inventory_obj = IngredientInventory.objects.get(ingredient_name = ingredient.ingredient)
                inventory_obj.ingredient_quantity -= qty_required
                inventory_obj.save()
            return HttpResponseRedirect('/purchase_log')
        return render(request, self.template_name, {'form': form})

class PurchaseUpdate(LoginRequiredMixin, UpdateView):
    model = PurchaseLog
    template_name = "inventory_tracker/purchase_update.html"
    form_class = PurchaseForm

class PurchaseDelete(LoginRequiredMixin, DeleteView):
    model = PurchaseLog
    template_name = "inventory_tracker/purchase_delete.html"
    success_url = "/purchase_log"