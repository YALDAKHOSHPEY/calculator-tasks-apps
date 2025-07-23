from django.urls import path
from . import views

app_name = 'tasks'
urlpatterns = [
    path('', views.index, name='index'),
    path('add/', views.add, name='add'),
    path('edit/<int:task_index>/', views.edit, name='edit'),
    path('delete/<int:task_index>/', views.delete, name='delete'),
]