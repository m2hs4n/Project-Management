import os
import pika
from tasks import send_email_task

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.develop')
# django.setup()

def callback(ch, method, properties, body):
    email_data = body.decode('utf-8').split(',')
    subject = email_data[0]
    message = email_data[1]
    from_email = email_data[2]
    recipient_list = email_data[3].split(';')
    # Call the send_email_task
    send_email_task.delay(subject, message, from_email, recipient_list)


def main():
    connection = pika.BlockingConnection(pika.ConnectionParameters('rabbitmq'))
    
    # Task consumer
    channel = connection.channel()
    channel.queue_declare(queue='tasks_send_email_queue')
    channel.basic_consume(queue='tasks_send_email_queue', on_message_callback=callback, auto_ack=True)
    print('Waiting for messages. To exit press CTRL+C')
    channel.start_consuming()
    
if __name__ == '__main__':
    main()