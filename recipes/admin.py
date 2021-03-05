from django.contrib import admin

from .models import Recipe, Ingredient, Tag, Follow, IngredientsInRecipe, TagsInRecipe


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


# class GroupAdmin(admin.ModelAdmin):
#     list_display = (
#         'title',
#         'slug',
#         'description',
#     )
#     search_fields = ('description',)
#     empty_value_display = '-пусто-'


# class CommentAdmin(admin.ModelAdmin):
#     list_display = (
#         'pk',
#         'post',
#         'text',
#         'author',
#         'created',
#     )
#     search_fields = ('text',)
#     list_filter = ('created',)
#     empty_value_display = '-пусто-'


class FollowAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'author',
        'user',
    )
    search_fields = ('author', 'user',)


# admin.site.register(Post, PostAdmin)
# admin.site.register(Group, GroupAdmin)
admin.site.register(Recipe, RecipeAdmin)
admin.site.register(Follow, FollowAdmin)
