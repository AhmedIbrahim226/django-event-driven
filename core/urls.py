"""
URL configuration for core project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from progress.views import ProgressesView, pause_progress_view, continue_progress_view, restart_progress_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', ProgressesView.as_view(), name='progresses'),
    path('pause/progress/task/<progress_id>/<current_percentage>/', pause_progress_view),
    path('continue/progress/task/<progress_id>/', continue_progress_view),
    path('restart/progress/task/<progress_id>/', restart_progress_view),
]
