from django.contrib.auth.tokens import default_token_generator
from django.shortcuts import get_object_or_404
from rest_framework.relations import SlugRelatedField
from rest_framework.serializers import (CharField, CurrentUserDefault,
                                        IntegerField, ModelSerializer,
                                        Serializer, SlugField, ValidationError)
from reviews.models import Category, Comment, Genre, Review, Title, User


class CategorySerializer(ModelSerializer):

    class Meta:
        model = Category
        exclude = ('id',)


class CommentSerializer(ModelSerializer):
    author = SlugRelatedField(
        read_only=True,
        slug_field='username'
    )

    class Meta:
        model = Comment
        fields = ('id', 'text', 'author', 'pub_date',)


class CreateUpdateDestroyTitleSerializer(ModelSerializer):
    genre = SlugRelatedField(
        many=True,
        slug_field='slug',
        queryset=Genre.objects.all()
    )
    category = SlugRelatedField(
        slug_field='slug',
        queryset=Category.objects.all()
    )

    class Meta:
        model = Title
        fields = ('id', 'name', 'year', 'description', 'genre', 'category',)


class GenreSerializer(ModelSerializer):

    class Meta:
        model = Genre
        exclude = ('id',)


class ListRetrieveTitleSerializer(ModelSerializer):
    genre = GenreSerializer(many=True)
    category = CategorySerializer()
    rating = IntegerField(source='reviews__score__avg', read_only=True)

    class Meta:
        model = Title
        fields = ('id', 'name', 'year', 'rating', 'description',
                  'genre', 'category',)


class ReviewSerializer(ModelSerializer):
    title = SlugRelatedField(
        read_only=True,
        slug_field='name'
    )
    author = SlugRelatedField(
        read_only=True,
        slug_field='username',
        default=CurrentUserDefault()
    )

    def validate(self, data):
        author = self.context['request'].user
        title = get_object_or_404(
            Title, pk=self.context['view'].kwargs.get('title_id'))
        if self.context['request'].method == 'POST':
            if Review.objects.filter(title=title, author=author).exists():
                raise ValidationError('На каждое произведение Вы можете '
                                      'добавить только один отзыв!')
        return data

    class Meta:
        model = Review
        fields = ('id', 'text', 'author', 'score', 'pub_date', 'title',)


class SignUpSerializer(ModelSerializer):

    def validate_username(self, value):
        if value.lower() != 'me':
            return value
        raise ValidationError('Запрещенный username')

    class Meta:
        model = User
        fields = ('email', 'username')


class TokenSerializer(Serializer):
    confirmation_code = CharField(required=True, max_length=50)
    username = CharField(required=True, max_length=150)

    def validate(self, attrs):
        user = get_object_or_404(User, username=attrs['username'])
        if default_token_generator.check_token(
            user,
            attrs['confirmation_code']
        ):
            return attrs
        raise ValidationError('Некорретный токен')


class UserSerializer(ModelSerializer):

    class Meta:
        model = User
        fields = (
            'username',
            'email',
            'first_name',
            'last_name',
            'bio',
            'role'
        )


class UserProfileSerializer(UserSerializer):
    role = SlugField(required=False, read_only=True)
