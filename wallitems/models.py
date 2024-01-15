from django.db import models
from django.contrib.auth.models import User


class WallItem(models.Model):
    """
    Model for user Wall
    """
    
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="wallitem_owner")
    message = models.TextField(blank=False, null=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.message