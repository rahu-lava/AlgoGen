import random
from django.core.management.base import BaseCommand
from faker import Faker
from credentials.models import user_table
from dashboard.models import Resume

fake = Faker()

class Command(BaseCommand):
    help = "Generate fake user and resume data"

    def add_arguments(self, parser):
        parser.add_argument(
            "--count", type=int, default=10, help="Number of fake users to create"
        )

    def handle(self, *args, **options):
        count = options["count"]
        self.stdout.write(self.style.SUCCESS(f"Creating {count} fake users and resumes..."))

        for _ in range(count):
            user = user_table.objects.create(
                first_name=fake.first_name(),
                last_name=fake.last_name(),
                email=fake.unique.email(),
                password="password123",  # Use a default password or hash it
            )

            Resume.objects.create(
                user=user,
                skills=", ".join(fake.words(nb=5)),  # Random skills
                experience=random.randint(0, 15),  # Random experience years
                position=fake.job(),
                keywords=", ".join(fake.words(nb=5)),
                english_level=random.randint(1, 5),
                current_rating=str(random.randint(20, 100))
            )

        self.stdout.write(self.style.SUCCESS(f"Successfully created {count} users and resumes!"))
