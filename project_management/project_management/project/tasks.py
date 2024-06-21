import json

import pika

import datetime

from celery import shared_task

from project_management.project.models import Task


@shared_task
def check_tasks():
    """
        The `check_tasks` function is a Celery shared task designed to check for pending tasks due the next day and send notifications for these tasks via a RabbitMQ message queue.

        Steps performed by this function:
        1. Calculate the date for tomorrow.
        2. Retrieve tasks from the database that have a status of 'PENDING' and are due tomorrow.
        3. Establish a connection to the RabbitMQ server running on the host 'rabbitmq'.
        4. Declare a durable queue named 'tasks_send_email_queue' to ensure persistence.
        5. For each task that matches the criteria, create a JSON message containing the task's email, title, status, and due date.
        6. Publish the message to the 'tasks_send_email_queue'.
        7. Close the connection to RabbitMQ.

        This function enables the system to automatically send reminders for tasks that are due soon, helping ensure that users are notified in a timely manner.
    """
    tomorrow = datetime.date.today() + datetime.timedelta(days=1)
    tasks = Task.objects.filter(status=Task.Status.PENDING, due_date=tomorrow)
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='rabbitmq'))
    channel = connection.channel()
    channel.queue_declare(queue='tasks_send_email_queue', durable=True)
    for task in tasks:
        body = json.dumps({
            "email": "test@gmail.com",
            "title": str(task.title),
            "status": str(task.status),
            "due_date": str(task.due_date),
        })
        channel.basic_publish(exchange='', routing_key='tasks_send_email_queue', body=body)
    connection.close()
