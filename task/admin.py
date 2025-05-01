from django.contrib import admin
from .models import ToDo, ToDoUser
# Register your models here.
admin.site.register(ToDo)
admin.site.register(ToDoUser)