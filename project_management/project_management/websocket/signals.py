from asgiref.sync import async_to_sync

from channels.layers import get_channel_layer

from django.dispatch.dispatcher import receiver
from django.db.models.signals import post_save

from project_management.project.models import Task


@receiver(post_save, sender=Task)
def task_post_save(sender, instance, **kwargs):
    """
        send notification when a task is created or change status
    """
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)("test", {
        "type": "send_notification",
        "status": f"{instance.status}",
        "project": f"{instance.project.name}",
        "title": f"{instance.title}",
        "due_date": f"{instance.due_date}",
    })
