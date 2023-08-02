from django.db import models


class ProgressStatus(models.Model):
    target_value = models.SmallIntegerField()
    info = models.TextField()
    # rate_increase = models.SmallIntegerField()
    current_percentage = models.SmallIntegerField(default=0)
    status = models.SmallIntegerField(choices=[(1, 'Loading'), (2, 'Paused'), (3, 'Finished')], default=1)


class WebsocketClient(models.Model):
    progress = models.OneToOneField(ProgressStatus, on_delete=models.CASCADE)
    channel_name = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return self.channel_name if self.channel_name else 'None'


class TaskInfo(models.Model):
    uuid = models.CharField(max_length=100, unique=True)
    name = models.CharField(max_length=20, unique=True)
    
    def __str__(self):
        return self.uuid