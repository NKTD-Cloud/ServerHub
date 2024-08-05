![NKTDCLOUD Logo](https://github.com/NKTD-Cloud/.github/blob/main/images/logo.png)

# NKTD.CLOUD ServerHub

NKTD.CLOUD ServerHub ist eine Flask-basierte Webanwendung zur Verwaltung und Anzeige von Serverinformationen. Diese Anwendung umfasst Benutzeranmeldung, Serverdetails und Downloadfunktionen sowie Fehlerbehandlung und Sicherheitsmaßnahmen.

## Inhaltsverzeichnis

- [Installation](#installation)
- [Konfiguration](#konfiguration)
- [Ausführung](#ausführung)
- [Docker](#docker)
- [Fehlerbehandlung](#fehlerbehandlung)
- [Sicherheit](#sicherheit)
- [Lizenz](#lizenz)

## Installation

1. **Repository klonen:**

    ```bash
    git clone https://github.com/NKTD-Cloud/ServerHub.git
    cd ServerHub
    ```

2. **Virtuelle Umgebung erstellen und aktivieren:**

    ```bash
    python3 -m venv venv
    source venv/bin/activate  # Auf Windows: venv\Scripts\activate
    ```

3. **Abhängigkeiten installieren:**

    ```bash
    pip install -r requirements.txt
    ```

## Konfiguration

Die Anwendung verwendet eine Konfigurationsdatei (`config.py`), um Umgebungsvariablen und Einstellungen zu verwalten. Standardmäßig gibt es zwei Konfigurationen: `DevelopmentConfig` und `ProductionConfig`.

Um die gewünschte Konfiguration zu setzen, die Umgebungsvariable `FLASK_ENV` wie folgt einstellen:

```bash
export FLASK_ENV=development  # Für Entwicklungsumgebung
export FLASK_ENV=production   # Für Produktionsumgebung
```

## Ausführung

1. **Anwendung starten:**

    ```bash
    flask run
    ```

    Die Anwendung wird standardmäßig auf `http://127.0.0.1:5000` ausgeführt.

## Docker

Die Anwendung kann auch mit Docker ausgeführt werden.

1. **Docker-Image erstellen:**

    ```bash
    docker build -t nktd-cloud-serverhub .
    ```

2. **Docker-Container starten:**

    ```bash
    docker run -p 8000:8000 nktd-cloud-serverhub
    ```

Alternativ kann Docker Compose verwendet werden:

1. **Docker Compose starten:**

    ```bash
    docker-compose up
    ```

    Die Anwendung wird auf `http://localhost:8000` ausgeführt.

## Fehlerbehandlung

Die Anwendung behandelt verschiedene HTTP-Fehler und zeigt benutzerdefinierte Fehlerseiten an:

- 400 Bad Request
- 403 Forbidden
- 404 Not Found
- 429 Too Many Requests
- 500 Internal Server Error
- 502 Bad Gateway
- 503 Service Unavailable

## Sicherheit

Die Anwendung enthält mehrere Sicherheitsmaßnahmen, darunter:

- CSRF-Schutz mit Flask-WTF
- Passwort-Hashing mit Flask-Bcrypt
- Ratenbegrenzung mit Flask-Limiter
- Sicherheitsheader mit `set_security_headers`-Middleware

## Lizenz

Diese Anwendung ist unter der MIT-Lizenz lizenziert. Weitere Informationen sind in der `LICENSE`-Datei zu finden.
