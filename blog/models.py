from django.db import models
from bookings.models import Service

class Blog(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    # service = models.ForeignKey(Service, on_delete=models.CASCADE, null=True, blank=True, related_name='blogs')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
