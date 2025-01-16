from django.db import models
from django.contrib.auth.models import User


class JournalEntry(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="journal_entries"
    )
    date = models.DateField(auto_now_add=True)
    content = models.TextField()
    concepts_learned = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-date"]
        unique_together = ["user", "date"]  # One entry per day per user

    def __str__(self):
        return f"{self.user}'s entry on {self.date}"
