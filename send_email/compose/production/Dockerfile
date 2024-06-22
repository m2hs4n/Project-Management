# Use the official Python image from the Docker Hub
FROM python:3.10-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set work directory
WORKDIR /app

RUN apt-get update \
    && apt-get install -y --no-install-recommends gcc libc-dev \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Install dependencies
COPY send_email/requirements /app/
RUN pip install --upgrade pip
RUN pip install -r production.txt

# Copy project
COPY send_email /app/

# Copy and set permission for running celery worker
COPY ./send_email/compose/production/celery/worker/start /start-celery-worker
RUN chmod +x /start-celery-worker

# Copy and set permission for running RabbitMQ consumer task
COPY ./send_email/compose/develop/consumer/start_summery /start-consumer-task
RUN chmod +x /start-consumer-task

# Copy and set permission for running RabbitMQ consumer summery
COPY ./send_email/compose/develop/consumer/start_summery /start-consumer-summery
RUN chmod +x /start-consumer-summery

# Copy and set permission for running celery flower
COPY ./send_email/compose/production/celery/flower/start /start-flower
RUN chmod +x /start-flower

# Add a user for security purposes
RUN adduser --disabled-password django-user
RUN chown -R django-user:django-user /app
USER django-user


# Expose the port the app runs on
EXPOSE 8000

# Migrate to database then run the application
CMD ["sh", "-c", "python manage.py makemigrations && python manage.py migrate && python manage.py runserver --production 0.0.0.0:8002"]
