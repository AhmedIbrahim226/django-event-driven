from .models import TaskInfo, ProgressStatus
from core.celery import app


class TaskInfoQueries:
    @staticmethod
    def create(**kwargs):
        TaskInfo.objects.create(**kwargs)

    @staticmethod
    def get_by_name(name):
        return TaskInfo.objects.get(name=name)

    @staticmethod
    def filter_by_name(name):
        return TaskInfo.objects.filter(name=name)

    def filter_by_name_then_delete(self, name):
        tasks = self.filter_by_name(name=name)
        tasks.delete()

    @staticmethod
    def filter_by_uuid_then_delete(task_id):
        TaskInfo.objects.filter(uuid=task_id).delete()

task_info_q = TaskInfoQueries()

class ProgressStatusQueries:

    @staticmethod
    def all_order_by_status():
        return ProgressStatus.objects.all().order_by('status')
    @staticmethod
    def filter_by_id(progress_id):
        return ProgressStatus.objects.filter(id=progress_id)
    @staticmethod
    def filter_by_id_then_update(progress_id, **kwargs):
        ProgressStatus.objects.filter(id=progress_id).update(**kwargs)

progress_status_q = ProgressStatusQueries()

def revoke_celery_task(task_id):
    app.control.revoke(task_id, terminate=True, signal='SIGKILL')

def pause_progress_task(progress_id, current_percentage):
    task = task_info_q.get_by_name(name=f'progress-status-{progress_id}')
    revoke_celery_task(task_id=task.uuid)
    progress_status_q.filter_by_id_then_update(progress_id=progress_id, current_percentage=current_percentage, status=2)
    task_info_q.filter_by_name_then_delete(name=f'progress-status-{progress_id}')


def continue_progress_task(progress_id):
    progress = progress_status_q.filter_by_id(progress_id=progress_id)
    progress.update(status=1)
    progress = progress.first()
    from .tasks import progresses_task
    progresses_task.apply_async((progress_id, progress.target_value, progress.status, progress.current_percentage))

def restart_progress_task(progress_id):
    progress = progress_status_q.filter_by_id(progress_id=progress_id)
    progress.update(status=1, current_percentage=0)
    progress = progress.first()
    from .tasks import progresses_task
    progresses_task.apply_async((progress_id, progress.target_value, progress.status))
