# Event Management API

## Overview

This project is a Django-based REST API designed to manage events such as conferences, meetups, and more. The API provides endpoints to create, view, update, and delete events, and also handles user registrations.

## Features

- **Event Management:** Create, read, update, and delete events.
- **User Registration and Authentication:** Basic user management to handle user registrations and logins.
- **API Documentation:** Comprehensive documentation of the API endpoints.
- **Docker Support:** Containerized deployment using Docker.
- **Bonus Features:**
  - Event search and filtering.
  - Email notifications to users upon event registration.

## Tech Stack

- **Django:** Web framework used for developing the API.
- **Django REST Framework (DRF):** Toolkit for building Web APIs.
- **PostgreSQL:** Database to store event and user data.
- **Docker:** Containerization for easy deployment and environment consistency.
- **Whitenoise:** Simplified static file serving for the web app.
- **drf-spectacular:** For API documentation.
- **allauth and dj-rest-auth:** To handle user registrations and logins.
- **Sentry:** For Error and Performance Monitoring

## Getting Started

### Prerequisites

- **Docker**: Ensure Docker is installed on your machine.

### Installation

1. **Clone the repository:**

    ```bash
    git clone https://github.com/YuriiKrav4enko/Django-event-management.git
    ```

2. **Set up environment variables and local settings:**

    Create a `.env` file in the project root for example `.env.example`.
    
    Create a `local.py` file in the `core/project/settings` folder for example `.local_example.py` for get access to Api Docs and use django console email backend.

3. **Build and run the Docker containers:**

    ```bash
    make backend-image
    ```

4. **Run migrations:**

    Inside the Docker container, apply migrations:

    ```bash
    make migrations
    ```

5. **Create a superuser:**

    ```bash
    make superuser
    ```

6. **Stop the Docker containers:**

    ```bash
    make backend-stop
    ```

Also you can up only database `make db` and run project locally with `./manage.py runserver`.


### Usage

- **API Documentation:** Access Swagger documentation at `http://localhost:8000/api/schema/swagger-ui/`.
- **Admin Panel:** Visit `http://localhost:8000/admin/` to manage events and users.


### Implemented `Make` Commands

* `make backend-image` - build app docker image
* `make backend` - up application and database/infrastructure
* `make backend-logs` - follow the logs in app container
* `make backend-stop` - down application and all infrastructure
* `make db` - up only storages. you should run your application locally for debugging/developing purposes
* `make db-logs` - foolow the logs in storages containers
* `make db-stop` - down all infrastructure
