from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator
from recipes.models import Follow, User


class FollowSerializer(serializers.ModelSerializer):
    user = serializers.SlugRelatedField(
        slug_field='username',
        # read_only=True,
        queryset=User.objects.all(),
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
