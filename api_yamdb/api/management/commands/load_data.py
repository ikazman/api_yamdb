import csv
import os

from reviews.models import Category, Comment, Review
from django.core.management import BaseCommand


TABLES_DICT = {
    Category: 'category.csv',
    Review: 'review.csv',
    Comment: 'comments.csv',
}


class Command(BaseCommand):
    """Загружает csv в базу данных."""

    def add_arguments(self, parser):
        parser.add_argument('--path', type=str)

    def handle(self, *args, **kwargs):
        path = kwargs['path']
        for table, file in TABLES_DICT.items():
            filename = os.path.join(path, file)
            with open(filename, 'r') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    data = dict((key.lower(), value) for
                                key, value in row.items())
                    model_instance = table(**data)
                    model_instance.save()
