from django.contrib import admin

from .models import Category, Comment, Genre, Review, Title, User


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'slug',)
    search_fields = ('name', 'slug',)
    list_editable = ('name', 'slug',)


class CommentAdmin(admin.ModelAdmin):
    list_display = ('id', 'text', 'author', 'pub_date', 'review',)
    search_fields = ('text', 'author', 'pub_date', 'review',)
    list_filter = ('author', 'pub_date', 'review',)
    list_editable = ('text',)


class GenreAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'slug',)
    search_fields = ('name', 'slug',)
    list_editable = ('name', 'slug',)


class ReviewAdmin(admin.ModelAdmin):
    list_display = ('id', 'text', 'author', 'score', 'pub_date', 'title',)
    search_fields = ('text', 'author', 'score', 'pub_date', 'title',)
    list_filter = ('author', 'score', 'pub_date', 'title',)
    list_editable = ('text',)
    empty_value_display = '-пусто-'


class TitleAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'year', 'description', 'category',)
    search_fields = ('name', 'year', 'description', 'genre', 'category',)
    list_filter = ('year', 'genre', 'category',)
    list_editable = ('name', 'year', 'description', 'category',)
    empty_value_display = '-пусто-'


class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'username', 'email', 'first_name', 'last_name',
                    'bio')
    search_fields = ('username',)
    empty_value_display = '-пусто-'


admin.site.register(Category, CategoryAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Genre, GenreAdmin)
admin.site.register(Review, ReviewAdmin)
admin.site.register(Title, TitleAdmin)
admin.site.register(User, UserAdmin)
