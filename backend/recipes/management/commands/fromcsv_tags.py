from django.core.management.base import BaseCommand

from recipes.models import Tag


class Command(BaseCommand):
    help = 'Переносим теги'

    def handle(self, *args, **options):
        data = [
            {'name': 'Завтрак', 'color': '#9bc8d1', 'slug': 'breakfast'},
            {'name': 'Обед', 'color': '#557d52', 'slug': 'lunch'},
            {'name': 'Ужин', 'color': '#dabfc4', 'slug': 'diner'},
        ]
        Tag.objects.bulk_create(Tag(**tag) for tag in data)
        self.stdout.write(self.style.SUCCESS('Теги загрузились!'))
