from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from rest_framework import serializers
from rest_framework.fields import CurrentUserDefault
from rest_framework.validators import ValidationError

from main.models import Category, Genre, Title, Review, Comment

User = get_user_model()


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        exclude = ['id']


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        exclude = ['id']


class TitleSerializerGET(serializers.ModelSerializer):
    genre = GenreSerializer(many=True, )
    category = CategorySerializer()
    rating = serializers.IntegerField(required=False)

    class Meta:
        model = Title
        fields = '__all__'
        read_only_fields = ['rating', ]


class TitleSerializerPOST(TitleSerializerGET):
    genre = serializers.SlugRelatedField(slug_field='slug',
                                         queryset=Genre.objects.all(),
                                         many=True)
    category = serializers.SlugRelatedField(slug_field='slug',
                                            queryset=Category.objects.all(),
                                            required=False)


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(queryset=User.objects.all(),
                                          slug_field='username',
                                          default=CurrentUserDefault()
                                          )

    class Meta:
        model = Review
        fields = ['id', 'text', 'author', 'score', 'pub_date']
        read_only_fields = ['author']

    def validate(self, data):
        if self.context.get('request').method == 'POST':
            title_id = self.context.get('view').kwargs.get('title_id')
            title = get_object_or_404(Title, id=title_id)
            if title.reviews.filter(author=self.context.get('request').user):
                raise ValidationError(
                    {'author': 'Вы уже делали review для этого title'}
                )
        return data


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(slug_field='username',
                                          queryset=User.objects.all(),
                                          default=CurrentUserDefault()
                                          )

    class Meta:
        model = Comment
        fields = '__all__'
        read_only_fields = ['review', 'author']
