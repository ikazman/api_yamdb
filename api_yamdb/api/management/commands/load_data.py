import csv
import os

from reviews.models import Category, Comment, Review

from django.core.management import BaseCommand

from reviews.models import Category
from users.models import User


TABLES_DICT = {User: 'users.csv',
               Category: 'category.csv',
               Review: 'review.csv',
               Comment: 'comments.csv',
               }

FIELDS_WITH_ID = {'review_id': 'review',
                  'title_id': 'title',
                  'genre_id': 'genre'}


class Command(BaseCommand):
    """Загружает csv в базу данных."""

    def add_arguments(self, parser):
        parser.add_argument('--path', type=str)

    def handle(self, *args, **kwargs):
        path = kwargs['path']
        for table, file in TABLES_DICT.items():
            filename = os.path.join(path, file)
            with open(filename, 'r', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    data = dict((key.lower(), value) for
                                key, value in row.items())
                    for key, value in data.items():
                        if key in FIELDS_WITH_ID:
                            key = FIELDS_WITH_ID[key]
                            data[key] = value
                    model_instance = table(**data)
                    model_instance.save()
