from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    email = models.EmailField(max_length=255, unique=True)
    first_name = models.CharField(max_length=30, blank=True, null=True)

    # Remove username field entirely
    username = None
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []  # No extra required fields

    def __str__(self):
        return f"{self.first_name} ({self.email})" if self.first_name else self.email
    
class Poll(models.Model):
    creator = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='polls')
    question = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.question

class Option(models.Model):
    poll = models.ForeignKey(Poll, on_delete=models.CASCADE, related_name='options')
    text = models.CharField(max_length=100)
    votes = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.text

class Vote(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    option = models.ForeignKey(Option, on_delete=models.CASCADE)
    voted_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'option')  # Ensures one vote per user per poll option