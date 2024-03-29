from django.urls import path

from . import views

app_name = 'recipes'

urlpatterns = [
    path('', views.Index.as_view(), name='index'),
    path('new_recipe/', views.new_recipe, name='new_recipe'),
    path('author/<str:username>/', views.AuthorList.as_view(), name='author'),
    path('favorite/', views.FavoriteList.as_view(), name='favorite'),
    path('recipe/<slug:slug>/', views.RecipeDetail.as_view(), name='recipe'),
    path('recipe/<slug:slug>/edit/', views.recipe_edit, name='recipe_edit'),
    path('recipe/<slug:slug>/delete/', views.recipe_delete, name='recipe_delete'),
    path('follow/', views.FollowList.as_view(), name='follow'),
    path('purchase/', views.PurchaseList.as_view(), name='purchase'),
    path('purchase/download', views.PurchaseListDownload, name='purchase_download'),
    path('purchase/<slug:slug>/delete/', views.purchase_delete, name='purchase_delete'),
]
