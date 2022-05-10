#!/usr/bin/env python3
"""A Basic Flask app with internationalization support.
"""
import re
from flask import Flask, render_template, request, g
from flask_babel import Babel


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
    locale = request.args.get('locale', '')
    if locale in app.config["LANGUAGES"]:
        return locale
    user_details = getattr(g, 'user', None)
    if user_details is not None:
        if user_details['locale'] in app.config["LANGUAGES"]:
            return user_details['locale']
    langs = re.split('[,;]', str(request.accept_languages))
    for lang in langs:
        if lang in app.config["LANGUAGES"]:
            return lang
    return app.config['BABEL_DEFAULT_LOCALE']


@app.route('/')
def get_index():
    """The home/index page.
    """
    user_details = getattr(g, 'user', None)
    ctxt = {
        'login_details': user_details,
    }
    return render_template('6-index.html', **ctxt)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
