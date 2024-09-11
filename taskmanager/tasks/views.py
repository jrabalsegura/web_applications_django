from django.shortcuts import render
from .models import Task
from .forms import TaskForm, ContactForm
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, FormView
from django.urls import reverse_lazy
from . import services
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import redirect
from datetime import date
from collections import defaultdict
# Create your views here.

def task_home(request):
    tasks = Task.objects.filter(status__in=["UNASSIGNED", "IN_PROGRESS", "DONE", "ARCHIVED"])
    
    context = defaultdict(list)
    for task in tasks:
        if task.status == "UNASSIGNED":
            context['unassigned_tasks'].append(task)
        elif task.status == "IN_PROGRESS":
            context['in_progress_tasks'].append(task)
        elif task.status == "DONE":
            context['done_tasks'].append(task)
        elif task.status == "ARCHIVED":
            context['archived_tasks'].append(task)
            
    return render(request, 'tasks/home.html', context)

def task_by_date(request: HttpRequest, by_date: date) -> HttpResponse:
    tasks = services.get_tasks_by_date(by_date)
    context = {'tasks': tasks}
    return render(request, 'task_list.html', context)

def create_task_on_sprint(request: HttpRequest, sprint_id: int) -> HttpResponseRedirect:
    if request.method == 'POST':
        task_data: dict[str, str] = {
            'title': request.POST['title'],
            'description': request.POST.get('description', ''),
            'status': request.POST.get('status', 'UNASSIGNED'),
        }
        task = services.create_task_and_add_to_sprint(task_data, sprint_id, request.user)
        return redirect('task-detail', task_id=task.id)
    raise Http404("Not found")

class TaskListView(ListView):
    model = Task
    template_name = 'task_list.html'
    context_object_name = 'tasks'

class TaskDetailView(DetailView):
    model = Task
    template_name = 'task_detail.html'
    context_object_name = 'task'
    
class TaskCreateView(CreateView):
    model = Task
    template_name = 'tasks/task_form.html'
    form_class = TaskForm
    
    def get_success_url(self):
        return reverse_lazy('tasks:task-detail', kwargs={'pk': self.object.id})

class TaskUpdateView(UpdateView):
    model = Task
    template_name = 'task_form.html'
    fields = ("name", "description", "start_date", "end_date")
    
    def get_success_url(self):
        return reverse_lazy('tasks:task-detail', kwargs={'pk': self.object.id})
    
class TaskDeleteView(DeleteView):
    model = Task
    template_name = 'task_confirm_delete.html'
    success_url = reverse_lazy('tasks:task-list')
    
class ContactFormView(FormView):
    template_name = 'tasks/contact_form.html'
    form_class = ContactForm
    success_url = reverse_lazy('tasks:contact-success')
    
    def form_valid(self, form):
        subject = form.cleaned_data.get('subject')
        message = form.cleaned_data.get('message')
        from_email = form.cleaned_data.get('from_email')
        
        services.send_contact_email(subject, message, from_email, ['admin@example.com'])
        
        return super().form_valid(form)

