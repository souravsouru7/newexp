from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class Expense(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name=models.CharField(max_length=200)
    amount=models.IntegerField()
    category=models.CharField(max_length=2000)
    date=models.DateField(auto_now=True)

    def __str__(self):
        return self.name
