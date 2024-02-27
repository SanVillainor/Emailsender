from django.contrib.auth.models import User
from django.db import models

class Mails(models.Model):
    PROGRESS_CHOICES = [
        ('sending', 'Sending'),
        ('sent', 'Sent'),
        ('failed', 'Failed'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    subject = models.CharField(max_length=255)
    content = models.TextField(default="")
    recipients = models.TextField()
    progress = models.CharField(max_length=20, choices=PROGRESS_CHOICES, default='sending')
    datetime = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.subject
