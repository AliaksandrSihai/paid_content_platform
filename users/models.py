from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.validators import RegexValidator

NULLABLE = {'null': True, 'blank': True}


class User(AbstractUser):
    """User's model"""

    number_validator = RegexValidator(regex=[r'^\+\d{9,15}$'],
                                      message='Phone number should start from "+" and consists of 9-15 digits')

    username = None
    phone = models.CharField(max_length=15, verbose_name='phone', unique=True, validators=[number_validator])
    email = models.EmailField(unique=True, verbose_name='email', **NULLABLE)
    city = models.CharField(max_length=135, verbose_name='city', **NULLABLE)
    avatar = models.ImageField(upload_to='users/', verbose_name='avatar', **NULLABLE)

    USERNAME_FIELD = "phone"
    REQUIRED_FIELDS = []

