from django.db import models

# Create your models here.
class Lead(models.Model):
    name = models.CharField(max_length=100, blank=True, null=True)
    email = models.CharField(max_length=100)
    phone = models.CharField(max_length=500, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.email