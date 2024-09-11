from django.http import HttpResponseBadRequest
from .services import can_add_task_to_sprint

class SprintTaskWithinRangeMixin:
    
    def dispatch(self, request, *args, **kwargs):
        task = self.get_object() if hasattr(self, 'get_object') else None
        sprint_id = request.POST.get("sprint")
        
        if sprint_id:
            if task or request.method == "POST":
                if not can_add_task_to_sprint(task, sprint_id):
                    return HttpResponseBadRequest("Task is not within sprint range")
        
        return super().dispatch(request, *args, **kwargs)
