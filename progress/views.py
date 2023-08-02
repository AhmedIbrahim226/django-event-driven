from django.urls import reverse
from django.views.generic import  CreateView
from .models import ProgressStatus
from .forms import ProgressStatusForm
from .tasks import progresses_task
from django.shortcuts import redirect
from .utils import pause_progress_task, continue_progress_task, restart_progress_task, progress_status_q



class ProgressesView(CreateView):
    form_class = ProgressStatusForm
    model = ProgressStatus
    template_name = 'progresses.html'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx.update(progresses=progress_status_q.all_order_by_status())
        return ctx
    
    def form_valid(self, form):
        saved_form = super().form_valid(form)
        progresses_task.apply_async((form.instance.id, form.instance.target_value, form.instance.status))
        return saved_form
    
    def get_success_url(self):
        return reverse('progresses')


def pause_progress_view(request, progress_id, current_percentage):
    pause_progress_task(progress_id=progress_id, current_percentage=current_percentage)
    return redirect('progresses')


def continue_progress_view(request, progress_id):
    continue_progress_task(progress_id=progress_id)
    return redirect('progresses')


def restart_progress_view(request, progress_id):
    restart_progress_task(progress_id=progress_id)
    return redirect('progresses')
