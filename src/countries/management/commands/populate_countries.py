import json

from django.core.management.base import BaseCommand

from countries.models import Country


class Command(BaseCommand):
    help = 'Populate countries with flags and phone codes in the database'

    def handle(self, *args, **options):
        with open('countries/management/commands/countries.txt', 'r') as file:
            # Read the content of the file
            data = json.load(file)

        # Split the file content by commas and curly braces
        for element in data:
            Country.objects.create(code=element['code'], name=element['name'],
                                   flag=element['flag'], phone_code=element['dial_code'])
