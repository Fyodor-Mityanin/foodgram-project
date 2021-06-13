from rest_framework import serializers

from recipes.models import Favorite, Follow, Ingredient, Purchase, Recipe, User


class FollowSerializer(serializers.ModelSerializer):

    def validate(self, data):
        user = self.context['request'].user
        author = data['author']
        if user == author:
            raise serializers.ValidationError('You cant follow yourself')
        return data

    user = serializers.SlugRelatedField(
        queryset=User.objects.all(),
        slug_field='username',
    )
    author = serializers.SlugRelatedField(
        queryset=User.objects.all(),
        slug_field='username',
    )

    class Meta:
        fields = ('user', 'author',)
        model = Follow
        validators = [
            serializers.UniqueTogetherValidator(
                queryset=Follow.objects.all(),
                fields=('user', 'author'),
                message=('This follow is already exist')
            )
        ]


class FavoriteSerializer(serializers.ModelSerializer):

    def validate(self, data):
        if Favorite.objects.filter(
            user=self.context['request'].user,
            recipe=data['recipe'],
        ).exists():
            raise serializers.ValidationError(
                'This Favorite is already exist'
            )
        return data
    user = serializers.SlugRelatedField(
        queryset=User.objects.all(),
        slug_field='username',
    )
    recipe = serializers.SlugRelatedField(
        queryset=Recipe.objects.all(),
        slug_field='title',
    )

    class Meta:
        fields = ('user', 'recipe',)
        model = Favorite


class PurchaseSerializer(serializers.ModelSerializer):

    def validate(self, data):
        if Purchase.objects.filter(
            user=self.context['request'].user,
            recipe=data['recipe'],
        ).exists():
            raise serializers.ValidationError(
                'This Purchase is already exist'
            )
        return data
    user = serializers.SlugRelatedField(
        queryset=User.objects.all(),
        slug_field='username',
    )
    recipe = serializers.SlugRelatedField(
        queryset=Recipe.objects.all(),
        slug_field='title',
    )

    class Meta:
        fields = ('user', 'recipe',)
        model = Purchase


class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ['title', 'dimension']
        model = Ingredient
