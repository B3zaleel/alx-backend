#!/usr/bin/env python3
"""A Basic Flask app with internationalization support.
"""
from flask import Flask, render_template, request, g
from flask_babel import Babel


class Config:
    """Represents a Flask Babel configuration.
    """
    LANGUAGES = ["en", "fr"]


app = Flask(__name__)
app.config_class = Config
app.config['LANGUAGES'] = Config.LANGUAGES
app.config['BABEL_DEFAULT_LOCALE'] = 'en'
app.config['BABEL_DEFAULT_TIMEZONE'] = 'UTC'
app.url_map.strict_slashes = False
babel = Babel(app)
users = {
    1: {"name": "Balou", "locale": "fr", "timezone": "Europe/Paris"},
    2: {"name": "Beyonce", "locale": "en", "timezone": "US/Central"},
    3: {"name": "Spock", "locale": "kg", "timezone": "Vulcan"},
    4: {"name": "Teletubby", "locale": None, "timezone": "Europe/London"},
}


def get_user(id=None):
    """Retrieves a user based on a user id.
    """
    try:
        return users.get(int(id), None)
    except Exception:
        return None


@app.before_request
def before_request():
    queries = request.query_string.decode('utf-8').split('&')
    query_table = dict(map(lambda x: x.split('='), queries))
    login_id = query_table.get('login_as', '')
    user = get_user(login_id)
    setattr(g, 'user', user)


@babel.localeselector
def get_locale():
    """Retrieves the locale for a web page.
    """
    queries = request.query_string.decode('utf-8').split('&')
    query_table = dict(map(lambda x: x.split('='), queries))
    locale = query_table.get('locale', '')
    if locale in app.config_class.LANGUAGES:
        return locale
    return request.accept_languages.best_match(app.config_class.LANGUAGES)


@app.route('/')
def get_index():
    """The home/index page.
    """
    user_details = getattr(g, 'user', None)
    ctxt = {
        'login_details': user_details,
    }
    return render_template('5-index.html', **ctxt)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
