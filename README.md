# Advanced Project Management Application

## Overview
This project is an advanced project management application designed to demonstrate proficiency in Django, microservices architecture, RESTful API development, asynchronous task processing, real-time notifications, and caching. The application uses Django, PostgreSQL, Celery, RabbitMQ, Redis, and WebSocket (Django Channels) to achieve these functionalities.

## Features
1. **Django project manager service**: The main service to handle project management for example CRUD APIs for both project and tasks. 
2. **Email service**: Consumes the events that sends by django to RabbitMQ queue to send email and summery

## Technologies Used
- Django
- Django REST Framework
- PostgreSQL
- Celery
- RabbitMQ
- Redis
- Django Channels
- Docker

## Description
This project is made with microservice architecture. This project has two parts, in the first part, a service has been created to manage the projects, where the user can define tasks, which will be sent to the users as a notification through the web socket if any status change task is done. Also, in this section, if a task is completed, it will be sent to the queue in the rabbitmq message broker. In the second part, all messages created in rabbitmq are received and sent to users through the Django email service.

## Setup Instructions

### Prerequisites
- Docker
- Docker Compose

### Installation
1. **Clone the repository:**
   ```bash
   git clone https://github.com/your-username/project-management-app.git
   cd project-management-app

2. **Run tests:**
   ``` bash
   docker compose -f docker-compose.tests.yml up

3. **Run the porject:**
   ``` bash
   docker compose -f docker-compose.production.yml up

### Run project for developing:
   ``` bash
   docker compose -f docker-compose.develop.yml up
