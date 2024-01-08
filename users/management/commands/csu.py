from django.core.management import BaseCommand

from users.models import User


class Command(BaseCommand):
    """Commad to create superuser"""

    def handle(self, *args, **options):
        user = User.objects.create(
            phone="+1234567890",
            first_name="Admin",
            last_name="Admin",
            is_staff=True,
            is_superuser=True,
            is_paid_subscribe=True,
        )
        user.set_password("123qwe456asd")
        user.save()
