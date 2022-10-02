import csv

from django.core.management.base import BaseCommand

from ...models import Category, Comment, Genre, Review, Title, User


class Command(BaseCommand):
    help = 'Команда для импорта данных из .csv файлов.'

    def handle(self, *args, **options):
        models_files_names = {
            User: 'users',
            Category: 'category',
            Genre: 'genre',
            Title: 'titles',
            Review: 'review',
            Comment: 'comments',
        }
        for model, file in models_files_names.items():
            with open(
                    f'static/data/{file}.csv',
                    newline='',
                    encoding='utf-8'
            ) as csv_file:
                datareader = csv.DictReader(csv_file, delimiter=',')
                model.objects.bulk_create([model(**row) for row in datareader])
                print(f'Импорт данных из файла static/data/{file}.csv '
                      f'прошел успешно!')
        self.add_genres_to_titles()

    def add_genres_to_titles(self):
        with open(
                'static/data/genre_title.csv',
                newline='',
                encoding='utf-8'
        ) as csv_file:
            datareader = csv.DictReader(csv_file, delimiter=',')
            for row in datareader:
                title = Title.objects.get(pk=row['title_id'])
                genre = Genre.objects.get(pk=row['genre_id'])
                title.genre.add(genre)
        print('Импорт данных из файла static/data/genre_title.csv '
              'прошел успешно!')
