from flask import Flask, render_template, redirect, url_for, session, flash, send_from_directory, abort, request
from flask_wtf import FlaskForm
from wtforms import PasswordField, SubmitField
from wtforms.validators import DataRequired
from flask_bcrypt import Bcrypt
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_wtf.csrf import CSRFProtect
import os
import json
import markdown2
from datetime import timedelta
import logging
from logging.handlers import RotatingFileHandler
from config import config

app = Flask(__name__)

env = os.getenv('FLASK_ENV', 'default')
app.config.from_object(config[env])

bcrypt = Bcrypt(app)
csrf = CSRFProtect(app)

limiter = Limiter(get_remote_address, app=app, default_limits=["5 per minute"])

if not os.path.exists('logs'):
    os.mkdir('logs')
file_handler = RotatingFileHandler('logs/app.log', maxBytes=10240, backupCount=10)
file_handler.setFormatter(logging.Formatter(
    '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'
))
file_handler.setLevel(logging.INFO)
app.logger.addHandler(file_handler)

app.logger.setLevel(logging.INFO)

# Hardcoded password hash (bcrypt hash of 'yourpassword')
hashed_password = bcrypt.generate_password_hash('pw').decode('utf-8')

with open('data/servers.json', encoding='utf-8') as f:
    server_data = json.load(f)

allowed_files = set()
for server in server_data['servers']:
    for download in server.get('downloads', []):
        url = download.get('url')
        if url:
            filename = os.path.basename(url)
            allowed_files.add(filename)


class LoginForm(FlaskForm):
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Anmelden')


@app.route('/login', methods=['GET', 'POST'])
@limiter.limit("10 per minute")
def login():
    form = LoginForm()
    if form.validate_on_submit():
        app.logger.info("Form validated")
        if bcrypt.check_password_hash(hashed_password, form.password.data):
            app.logger.info("Password matched")
            session['logged_in'] = True
            return redirect(url_for('dashboard'))
        else:
            app.logger.warning("Invalid password")
            flash('Falsches Passwort')
    else:
        app.logger.warning("Form not validated")
    return render_template('login.html', form=form)


@app.route('/')
@limiter.limit("30 per minute")
def index():
    return redirect(url_for('dashboard'))


@app.route('/dashboard')
@limiter.limit("30 per minute")
def dashboard():
    if not session.get('logged_in'):
        return redirect(url_for('login'))

    servers = server_data['servers']
    return render_template('server_list.html', servers=servers)


@app.route('/server/<int:server_id>')
@limiter.limit("30 per minute")
def server_detail(server_id):
    if not session.get('logged_in'):
        return redirect(url_for('login'))

    servers = server_data['servers']
    server = next((s for s in servers if s['id'] == server_id), None)
    if server is None:
        abort(404)

    if 'instructions' in server and server['instructions'] != "":
        server['instructions'] = markdown2.markdown(server['instructions'])

    return render_template('server_detail.html', server=server)


@app.route('/download/<filename>')
@limiter.limit("10 per minute")
def download(filename):
    if not session.get('logged_in'):
        return redirect(url_for('login'))

    if filename not in allowed_files:
        abort(403)

    return send_from_directory('static/downloads', filename, as_attachment=True)


@app.route('/logout')
@limiter.limit("10 per minute")
def logout():
    session.pop('logged_in', None)
    return redirect(url_for('login'))


@app.errorhandler(400)
def bad_request(e):
    return render_template('error.html', error_code=400, error_message="Bad Request",
                           error_description="Die Anfrage war ungültig."), 400


@app.errorhandler(403)
def forbidden(e):
    return render_template('error.html', error_code=403, error_message="Forbidden",
                           error_description="Es fehlt die Berechtigung, diese Seite zu sehen."), 403


@app.errorhandler(404)
def page_not_found(e):
    return render_template('error.html', error_code=404, error_message="Seite nicht gefunden",
                           error_description="Die angeforderte Seite konnte nicht gefunden werden."), 404


@app.errorhandler(429)
def too_many_requests(e):
    return render_template('error.html', error_code=429, error_message="Too Many Requests", error_description="Zu viele Anfragen in zu kurzer Zeit gesendet. Bitte versuche es später erneut."), 429


@app.errorhandler(500)
def internal_server_error(e):
    return render_template('error.html', error_code=500, error_message="Interner Serverfehler",
                           error_description="Es ist ein Fehler aufgetreten. Bitte versuche es später erneut."), 500


@app.errorhandler(502)
def bad_gateway(e):
    return render_template('error.html', error_code=502, error_message="Bad Gateway",
                           error_description="Der Server hat eine ungültige Antwort erhalten."), 502


@app.errorhandler(503)
def service_unavailable(e):
    return render_template('error.html', error_code=503, error_message="Service Unavailable",
                           error_description="Der Dienst ist derzeit nicht verfügbar. Bitte versuche es später erneut."), 503


@app.before_request
def make_session_permanent():
    session.permanent = True
    app.permanent_session_lifetime = timedelta(minutes=30)


@app.before_request
def before_request():
    if not request.is_secure and app.config['ENVIRONMENT'] == 'production':
        url = request.url.replace("http://", "https://", 1)
        return redirect(url, code=301)


@app.after_request
def set_security_headers(response):
    if app.config['ENVIRONMENT'] == 'production':
        response.headers['Content-Security-Policy'] = "default-src 'self'; script-src 'self'; style-src 'self';"
    else:
        response.headers[
            'Content-Security-Policy'] = "default-src 'self'; script-src 'self' 'unsafe-inline'; style-src 'self' 'unsafe-inline';"
    response.headers['X-Content-Type-Options'] = 'nosniff'
    response.headers['X-Frame-Options'] = 'DENY'
    response.headers['X-XSS-Protection'] = '1; mode=block'
    return response


if __name__ == '__main__':
    app.logger.info('Running in ' + app.config['ENVIRONMENT'])
    app.run(port=20015)
