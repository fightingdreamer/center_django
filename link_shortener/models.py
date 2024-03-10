from django.db import models


class Redirection(models.Model):
    hits = models.PositiveIntegerField(blank=False)
    location = models.CharField(max_length=1023, blank=False, unique=True)

    user_ip = models.GenericIPAddressField(blank=False)
    user_agent = models.CharField(max_length=1023, blank=True)

    class Meta:
        indexes = [
            models.Index(
                fields=[
                    "hits",
                ]
            ),
        ]
