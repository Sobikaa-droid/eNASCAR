from django.core.management import BaseCommand
from apps.racers.models import Racer


class Command(BaseCommand):
    def handle(self, *args, **options):
        username = input("Username: ")
        number = input("Number: ")
        password = input("Password: ")

        racer = Racer.objects.create(
            number=int(number),
            username=username,
            password=password,
            is_staff=True,
            is_superuser=True,
        )
        racer.set_password(password)
        racer.save()

        self.stdout.write("Successfully created super racer", ending="")
