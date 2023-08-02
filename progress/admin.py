from django.contrib import admin
from .models import ProgressStatus, WebsocketClient, TaskInfo

admin.site.register(ProgressStatus)
admin.site.register(WebsocketClient)
admin.site.register(TaskInfo)