from django.db import models
from django.contrib.auth.models import User
from pictures.models import Picture


class Likes(models.Model):
    """
    Likes model, related to User and Picture
    """
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    picture = models.ForeignKey(Picture, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)


    class Meta:
        ordering = ['-created_at']
        # Sets of field names that, taken together, must be unique
        unique_together = ['owner', 'picture']

    def __str__(self):
        return f'{self.owner} & {self.picture}'