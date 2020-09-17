from django.contrib.auth.models import AbstractUser
from django.db import models


PERSON = (
        ('dppc','dppc'),
        ('student','student'),
        ('staff','staff'),
        ('hod','hod'),
        ('faculty','faculty')
)

class CustomUser(AbstractUser):
    person = models.CharField(max_length=100,choices=PERSON,default='student')
