from celery import shared_task
from time import sleep
from .channels.broadcast_message import progress_broadcast_message
from asgiref.sync import async_to_sync
from .utils import progress_status_q, task_info_q



@shared_task(bind=True)
def progresses_task(self, progress_id, progress_target_value, status, continue_current_percentage=False):
    task_info_q.create(name=f'progress-status-{progress_id}', uuid=self.request.id)

    if not continue_current_percentage:
        sleep(1)
        i = 1
    else:
        i = int((continue_current_percentage / 100) * progress_target_value)
        
    while i <= progress_target_value:
        """Send message through websocket"""
        percentage = int((i / progress_target_value) * 100)
        async_to_sync(progress_broadcast_message)(progress_id, percentage, status)
        if percentage == 100:
            progress_status_q.filter_by_id_then_update(progress_id=progress_id, current_percentage=100, status=3)
            task_info_q.filter_by_uuid_then_delete(task_id=self.request.id)

        sleep(1)
        i += 1