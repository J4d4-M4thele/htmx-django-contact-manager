from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.validators import FileExtensionValidator
from django.conf import settings
from cloudinary.models import CloudinaryField

class User(AbstractUser):
    pass

class Contact(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    document = CloudinaryField(
        "document",
        blank=True,
        null=True,
        resource_type='raw',  # Important: specify 'raw' for documents
    )
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(
        User, 
        on_delete=models.CASCADE,
        related_name='contacts'
    )

    class Meta:
        unique_together = ('user', 'email')

    def __str__(self):
        return f"{self.name} <{self.email}>"    
    