from celery import shared_task

@shared_task
def example_task():
    print("This is an example task running every 10 seconds")
