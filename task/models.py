from django.db import models
from django.contrib.auth import get_user_model
# Create your models here.

status_choices = (
    ("Completed", "Completed"), 
    ("Pending", "Pending"), 
    ("Blocked" , "Blocked"),
)

priority_choices = (
    ("High", "High"), ("Mid","Mid"), ("Low","Low"),
)


class ToDoUser(models.Model):
    id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=255)
    
    def __str__(self):
        return self.username

class ToDo(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length= 100)
    desc = models.TextField()
    assigned_on = models.DateField(auto_now_add=True)
    priority = models.CharField(max_length=4, choices=priority_choices, default="Mid")
    status = models.CharField(max_length=10, choices=status_choices, default="Pending")
    user = models.ForeignKey(ToDoUser, on_delete=models.CASCADE)

    def __str__(self):
        return self.name
