from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home-page'),
    path('register/', views.register, name='registration'),
    path('login/', views.login, name='login'),
    path('logout/', views.logoutview, name='logout'),

    path('create-task/', views.createtask, name='Create Task'),
    path('task-list/', views.tasklist, name='Task List'),
    path('delete-task/<name>/', views.deletetask, name='delete'),
    path('edit/<int:id>', views.edit),
    path('view/<int:id>/', views.detailsview, name='view'),

]