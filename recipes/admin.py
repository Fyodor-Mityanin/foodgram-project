from django.contrib import admin

from .models import (Favorite, Follow, Ingredient, IngredientsInRecipe,
                     Purchase, Recipe, Tag, TagsInRecipe)


class RecipeAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'author',
        'title',
        'description',
        'slug',
        'time_to_cook',
    )
    search_fields = ('description',)
    list_filter = ('title',)
    empty_value_display = '-пусто-'


class IngredientAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'title',
        'dimension',
    )
    search_fields = ('title',)


class IngredientsInRecipeAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'recipe',
        'ingredient',
        'quantity'
    )
    search_fields = ('recipe', 'ingredient',)


class FollowAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'author',
        'user',
    )
    search_fields = ('author', 'user',)


class TagAdmin(admin.ModelAdmin):
    list_display = (
        'title',
        'slug',
        'color',
    )


class FavoriteAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'user',
        'recipe',
    )


class TagsInRecipeAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'tag',
        'recipe',
    )

class PurchaseAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'user',
        'recipe',
    )
   


admin.site.register(IngredientsInRecipe, IngredientsInRecipeAdmin)
admin.site.register(Ingredient, IngredientAdmin)
admin.site.register(Recipe, RecipeAdmin)
admin.site.register(Follow, FollowAdmin)
admin.site.register(Tag, TagAdmin)
admin.site.register(Favorite, FavoriteAdmin)
admin.site.register(TagsInRecipe, TagsInRecipeAdmin)
admin.site.register(Purchase, PurchaseAdmin)
