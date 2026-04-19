from django.db import models

# The student model.
class Student(models.Model):
    sir_name = models.CharField(max_length=100)
    first_name = models.CharField(max_length=100)
    joined_on = models.DateTimeField(auto_now_add=True)
