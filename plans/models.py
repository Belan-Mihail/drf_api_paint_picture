from django.db import models
from django.contrib.auth.models import User


class Plan(models.Model):
    """
    Model for user plans
    """
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="plan_owner")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    plans_title = models.CharField(max_length=255, blank=False)
    plans_description = models.TextField(max_length=300, blank=False)
    plans_date = models.DateField()
    until = models.BooleanField(default=False)
    
    
    class Meta:
        ordering = ['-created_at']


    def __str__(self):
        return f"{self.owner}'s plans"