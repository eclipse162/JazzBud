from django.db import models

# Create your models here.

class Token(models.Model):
    user = models.CharField(unique = True, max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    access_token = models.CharField(max_length=500)
    refresh_token = models.CharField(max_length=500)
    expires_in = models.DateTimeField()
    token_type = models.CharField(max_length=100)

    def __str__(self):
        return str(self.token)