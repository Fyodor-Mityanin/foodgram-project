from rest_framework import serializers

from recipes.models import Favorite, Follow, Ingredient, Purchase, Recipe, User


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
        validators = [
            serializers.UniqueTogetherValidator(
                queryset=Follow.objects.all(),
                fields=('user', 'author'),
                message=('This follow is already exist')
            )
        ]


class FavoriteSerializer(serializers.ModelSerializer):
    user = serializers.SlugRelatedField(
        queryset=User.objects.all(),
        slug_field='username',
    )
    recipe = serializers.SlugRelatedField(
        queryset=Recipe.objects.all(),
        slug_field='title',
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
        slug_field='title',
    )

    class Meta:
        fields = '__all__'
        model = Purchase


class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ['title', 'dimension']
        model = Ingredient