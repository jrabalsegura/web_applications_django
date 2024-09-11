from django.urls import path, register_converter
from django.views.generic import TemplateView
from .views import TaskListView, TaskCreateView, TaskDetailView, TaskUpdateView, TaskDeleteView
from . import views, converters

register_converter(converters.DateConverter, 'ddmmyyyy')

app_name = 'tasks'

urlpatterns = [
    path('', views.task_home, name='home'),
    path('help/', TemplateView.as_view(template_name='tasks/help.html'), name='help'),
    path('tasks/', TaskListView.as_view(), name='task-list'),
    path('tasks/new/', TaskCreateView.as_view(), name='task-create'),
    path('tasks/<int:pk>/', TaskDetailView.as_view(), name='task-detail'),
    path('tasks/<int:pk>/edit/', TaskUpdateView.as_view(), name='task-update'),
    path('tasks/<int:pk>/delete/', TaskDeleteView.as_view(), name='task-delete'),
    path('tasks/<ddmmyyyy:date>/', TaskListView.as_view(), name='task-by-date'),
    path('tasks/sprint/add_task/<int:pk>/', views.create_task_on_sprint, name='task-add-to-sprint'),
    path('tasks/home/', views.task_home, name='task-home'),
    path('contact/', views.ContactFormView.as_view(), name='contact'),
    path('contact-success/', TemplateView.as_view(template_name='tasks/contact_success.html'), name='contact-success'),
]