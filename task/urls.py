from django.urls import path
from .views import task_list, task_desc, task_delete, task_create, task_update, register, user_login,user_logout,  TaskViewSet
from rest_framework.routers import SimpleRouter

urlpatterns = [
    path("",task_list, name="task_list"),
    path("<int:id>", task_desc, name="task_desc"),
    path("new", task_create, name= "create"),
    path("<int:id>/delete", task_delete, name= "delete"),
    path("<int:id>/update", task_update, name= "update"),
    path("register", register, name="register"),
    path("accounts/login/", user_login, name="login"),
    path("login", user_login, name="login"),
    path("logout", user_logout, name= "logout")
]

router = SimpleRouter()

router.register('task-api', TaskViewSet)

urlpatterns += router.urls