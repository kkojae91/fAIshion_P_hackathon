import csv
import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mysite.settings")
django.setup()

from mysite.core.models import Book

hand = open('mysite/static/book_data/deeplearning_data.csv', encoding='cp949')
reader = csv.reader(hand)

bulk_list = []
for row in reader:
    bulk_list.append(Book(
        field = row[0],
        title = row[1],
        url = row[2],
        image_url = row[3],
    ))

Book.objects.bulk_create(bulk_list)

print("Complete !!")