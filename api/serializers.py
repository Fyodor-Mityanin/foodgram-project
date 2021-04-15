from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator
from recipes.models import Favorite, Follow, Ingredient, Purchase, User, Recipe


class FollowSerializer(serializers.ModelSerializer):
    user = serializers.SlugRelatedField(
        queryset=User.objects.all(),
        slug_field='username',
    )
    author = serializers.SlugRelatedField(
        queryset=User.objects.all(),
        slug_field='username',
    )

    class Meta:
        fields = '__all__'
        model = Follow


class FavoriteSerializer(serializers.ModelSerializer):
    user = serializers.SlugRelatedField(
        queryset=User.objects.all(),
        slug_field='username',
    )
    recipe = serializers.SlugRelatedField(
        queryset=Recipe.objects.all(),
        slug_field='slug',
    )

    class Meta:
        fields = '__all__'
        model = Favorite


class PurchaseSerializer(serializers.ModelSerializer):
    user = serializers.SlugRelatedField(
        queryset=User.objects.all(),
        slug_field='username',
    )
    recipe = serializers.SlugRelatedField(
        queryset=Recipe.objects.all(),
        slug_field='slug',
    )

    class Meta:
        fields = '__all__'
        model = Purchase


class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ['title', 'dimension']
        model = Ingredient
