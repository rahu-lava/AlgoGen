from django.db import models
from credentials.models import user_table
class Resume(models.Model):
    ENGLISH_LEVEL_CHOICES = [
        (0, "No English"),
        (1, "Basic"),
        (2, "Intermediate"),
        (3, "Fluent"),
    ]
    user = models.OneToOneField(user_table, on_delete=models.CASCADE, related_name='details',null=True)
    skills = models.TextField()
    experience = models.PositiveIntegerField()
    position = models.CharField(max_length=255)
    keywords = models.TextField(help_text="Enter keywords separated by commas")
    english_level = models.IntegerField(default='')
    current_rating = models.FloatField(blank=True, null=True)

    def __str__(self):
        return f"{self.position} ({self.experience} years)"
