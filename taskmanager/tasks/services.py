from .models import Sprint, Task
from django.shortcuts import get_object_or_404
from django.db import transaction
from django.core.exceptions import ValidationError
from datetime import datetime
from django.contrib.auth.models import User
from django.core.mail import send_mail


def can_add_task_to_sprint(task, sprint_id):
    
    sprint = get_object_or_404(Sprint, id=sprint_id)
    return sprint.start_date <= task.created_at.date() <= sprint.end_date

def create_task_and_add_to_sprint(task_data: dict[str, str], sprint_id: int, creator: User):   
    #Create a new task and associate it with a sprint
    
    sprint = Sprint.objects.get(id=sprint_id)
    
    now = datetime.now()
    
    if not (sprint.start_date <= now <= sprint.end_date):
        raise ValidationError("Task cannot be added to sprint outside the sprint date range")
    with transaction.atomic():
        task = Task.objects.create(title=task_data['title'], description=task_data.get['description', ''], status=task_data.get['status', 'UNASSIGNED'], creator=creator)
        sprint.tasks.add(task)
    return task

class TaskAlreadyClaimedException(Exception):
    pass

@transaction.atomic
def claim_task(user_id: int, task_id: int) -> None:
    
    #Lock the task row to prevent other transactions from claiming it simultaneously
    task = Task.objects.select_for_update().get(id=task_id)
    
    #Check if already claimed
    if task.owner_id:
        raise TaskAlreadyClaimedException("Task already claimed by another user")
    
    #Claim the task
    task.status = "IN_PROGRESS"
    task.owner_id = user_id
    task.save()
    
    #Hay una versión optimista en el libro Ultimate Django, Capítulo 5
    
def send_contact_email(subject: str, message: str, from_email: str, to_emails: list[str]) -> None:
    send_mail(subject, message, from_email, [to_emails])
