![NKTDCLOUD Logo](https://github.com/NKTD-Cloud/.github/blob/main/images/logo.png)

# ServerHub

NKTD.CLOUD ServerHub is a Flask-based web application for managing and displaying server information. This application includes user login, server details, and download features, as well as error handling and security measures.

## Table of Contents

- [Installation](#installation)
- [Configuration](#configuration)
- [Execution](#execution)
- [Docker](#docker)
- [Error Handling](#error-handling)
- [Security](#security)
- [License](#license)

## Installation

1. **Clone the repository:**

    ```bash
    git clone https://github.com/NKTD-Cloud/ServerHub.git
    cd ServerHub
    ```

2. **Create and activate a virtual environment:**

    ```bash
    python3 -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate
    ```

3. **Install dependencies:**

    ```bash
    pip install -r requirements.txt
    ```

## Configuration

The application uses a configuration file (`config.py`) to manage environment variables and settings. By default, there are two configurations: `DevelopmentConfig` and `ProductionConfig`.

To set the desired configuration, set the environment variable `FLASK_ENV` as follows:

```bash
export FLASK_ENV=development  # For development environment
export FLASK_ENV=production   # For production environment
```

## Execution

1. **Start the application:**

    ```bash
    flask run
    ```

    The application will run by default on `http://127.0.0.1:5000`.

## Docker

The application can also be run with Docker.

1. **Build the Docker image:**

    ```bash
    docker build -t nktd-cloud-serverhub .
    ```

2. **Start the Docker container:**

    ```bash
    docker run -p 8000:8000 nktd-cloud-serverhub
    ```

Alternatively, Docker Compose can be used:

1. **Start Docker Compose:**

    ```bash
    docker-compose up
    ```

    The application will run on `http://localhost:8000`.

## Error Handling

The application handles various HTTP errors and displays custom error pages:

- 400 Bad Request
- 403 Forbidden
- 404 Not Found
- 429 Too Many Requests
- 500 Internal Server Error
- 502 Bad Gateway
- 503 Service Unavailable

## Security

The application includes several security measures, including:

- CSRF protection with Flask-WTF
- Password hashing with Flask-Bcrypt
- Rate limiting with Flask-Limiter
- Security headers with `set_security_headers` middleware

## License

This application is licensed under the MIT License. For more information, see the `LICENSE` file.

