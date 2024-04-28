from django.core.management.base import BaseCommand
from stubdjango.urls import urlpatterns


class Command(BaseCommand):
    help = "テストコマンド"

    def handle(self, *args, **options):
        print(urlpatterns)
