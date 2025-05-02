from django.db import models

# models.py
class Method(models.Model):
    name = models.CharField(max_length=100)
    url = models.URLField(null=True, blank=True)
    selector = models.JSONField(null=True, blank=True)  # Optional, for inputs/buttons

    def __str__(self):
        return self.name
