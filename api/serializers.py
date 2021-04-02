from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator
from recipes.models import Favorite, Follow, User, Recipe


class FollowSerializer(serializers.ModelSerializer):
    user = serializers.SlugRelatedField(
        queryset=User.objects.all(),
        slug_field='username',
        # read_only=True,
        # default=serializers.CurrentUserDefault(),
    )
    author = serializers.SlugRelatedField(
        queryset=User.objects.all(),
        slug_field='username',
    )

    class Meta:
        fields = '__all__'
        model = Follow
        # validators = [
        #     UniqueTogetherValidator(
        #         queryset=Follow.objects.all(),
        #         fields=('user', 'author')
        #     )
        # ]


class FavoriteSerializer(serializers.ModelSerializer):
    user = serializers.SlugRelatedField(
        queryset=User.objects.all(),
        slug_field='username',
        # read_only=True,
        # default=serializers.CurrentUserDefault(),
    )
    recipe = serializers.SlugRelatedField(
        queryset=Recipe.objects.all(),
        slug_field='slug',
    )

    class Meta:
        fields = '__all__'
        model = Favorite
        # validators = [
        #     UniqueTogetherValidator(
        #         queryset=Follow.objects.all(),
        #         fields=('user', 'author')
        #     )
        # ]
