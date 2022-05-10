#!/usr/bin/env python3
"""A Basic Flask app with internationalization support.
"""
import re
import pytz
from flask import Flask, render_template, request, g
from flask_babel import Babel, format_datetime


class Config:
    """Represents a Flask Babel configuration.
    """
    LANGUAGES = ["en", "fr"]
    BABEL_DEFAULT_LOCALE = "en"
    BABEL_DEFAULT_TIMEZONE = "UTC"


app = Flask(__name__)
app.config.from_object(Config)
app.url_map.strict_slashes = False
babel = Babel(app)
users = {
    1: {"name": "Balou", "locale": "fr", "timezone": "Europe/Paris"},
    2: {"name": "Beyonce", "locale": "en", "timezone": "US/Central"},
    3: {"name": "Spock", "locale": "kg", "timezone": "Vulcan"},
    4: {"name": "Teletubby", "locale": None, "timezone": "Europe/London"},
}


def get_user():
    """Retrieves a user based on a user id.
    """
    login_id = request.args.get('login_as', '')
    try:
        if login_id:
            return users.get(int(login_id), None)
        return None
    except Exception:
        return None


@app.before_request
def before_request():
    """Performs some routines before each request's resolution.
    """
    user = get_user()
    setattr(g, 'user', user)


@babel.localeselector
def get_locale():
    """Retrieves the locale for a web page.
    """
    queries = request.query_string.decode('utf-8').split('&')
    query_table = dict(map(
        lambda x: (x if '=' in x else '{}='.format(x)).split('='),
        queries,
    ))
    locale = query_table.get('locale', '')
    if locale in app.config["LANGUAGES"]:
        return locale
    user_details = getattr(g, 'user', None)
    if user_details and user_details['locale'] in app.config["LANGUAGES"]:
        return user_details['locale']
    langs = re.split('[,;]', str(request.accept_languages))
    for lang in langs:
        if lang in app.config["LANGUAGES"]:
            return lang
    return app.config['BABEL_DEFAULT_LOCALE']


@babel.timezoneselector
def get_timezone():
    """Retrieves the timezone for a web page.
    """
    timezone = request.args.get('timezone', '').strip()
    user_details = getattr(g, 'user', None)
    if not timezone and user_details:
        timezone = user_details['timezone']
    try:
        return pytz.timezone(timezone)
    except pytz.exceptions.UnknownTimeZoneError:
        return pytz.timezone(app.config['BABEL_DEFAULT_TIMEZONE'])


@app.route('/')
def get_index():
    """The home/index page.
    """
    user_details = getattr(g, 'user', None)
    ctxt = {
        'login_details': user_details,
        'current_time': format_datetime(),
    }
    return render_template('index.html', **ctxt)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
