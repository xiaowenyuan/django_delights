from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.home, name="home"),
    path('menu/create', views.MenuItemCreate.as_view(), name = "menucreate"),
    path('menu/', views.MenuList.as_view(), name="menu_list"),
    path('menu/detail/<int:pk>', views.MenuDetail.as_view(), name="menu_detail"),
    path('menu/edit/<int:pk>', views.MenuItemUpdate.as_view(), name="menu_update"),
    path('menu/delete/<int:pk>', views.MenuItemDelete.as_view(), name="menu_delete"),
    path('recipe/', views.RecipeList.as_view(), name="recipe_list"),
    path('recipe/<int:pk>', views.RecipeDetail.as_view(), name="recipe_detail"),
    path('recipe/edit/<int:pk>', views.RecipeUpdate.as_view(), name="recipe_update"),
    path('recipe/delete/<int:pk>', views.RecipeDelete.as_view(), name="recipe_delete"),
    path('recipe/create', views.RecipeCreate.as_view(), name="recipe_create"),
    path('inventory/', views.InventoryList.as_view(), name="inventory_list"),
    path('inventory/create', views.InventoryCreate.as_view(), name="inventory_create"),
    path('inventory/edit/<int:pk>', views.InventoryUpdate.as_view(), name="inventory_update"),
    path('inventory/delete/<int:pk>', views.InventoryDelete.as_view(), name="inventory_delete"),
    path('purchase_log/', views.PurchaseLogList.as_view(), name="purchase_log_list"),
    path('purchase_log/create', views.PurchaseCreate.as_view(), name="purchase_create"),
    path('purchase_log/edit/<int:pk>', views.PurchaseUpdate.as_view(), name="purchase_update"),
    path('purchase_log/delete/<int:pk>', views.PurchaseDelete.as_view(), name="purchase_delete"),
    path("logout/", views.logout_view, name="logout"),
    path("signup/", views.SignUp.as_view(), name="signup"),
    path('accounts/', include("django.contrib.auth.urls"), name="login"),
]