#!/usr/bin/env python3
from flask import Flask, request, render_template, g

users = {
    1: {"name": "Balou", "locale": "fr", "timezone": "Europe/Paris"},
    2: {"name": "Beyonce", "locale": "en", "timezone": "US/Central"},
    3: {"name": "Spock", "locale": "kg", "timezone": "Vulcan"},
    4: {"name": "Teletubby", "locale": None, "timezone": "Europe/London"},
}


def get_locale():
    """
    Retrieves the locale from user data,
    request parameter, or defaults to 'en'.
    Returns:
        str: The chosen locale string
    """

    user = g.get('user')
    if user and user.get('locale'):
        return user['locale']

    locale_param = request.args.get('locale')
    if locale_param and locale_param in SUPPORTED_LOCALES:
        return SUPPORTED_LOCALES[locale_param]

    return 'en'


def get_user():
    """
    Retrieves the user dictionary from the
    login_as parameter, or None if not found.
    Returns:
        dict: The user dictionary or None if user not found.
    """

    login_as = request.args.get('login_as')
    if login_as and login_as.isdigit():
        user_id = int(login_as)
        return users.get(user_id)
    return None


@app.before_request
def before_request():
    """
    Sets the current user based on the login_as parameter before each request.
    """
    g.user = get_user()


@app.route('/')
def index():
    """home render function"""
    locale = get_locale()
    login_message = {
        'en': 'You are logged in as %(username)s.',
        'fr': 'Vous êtes connecté en tant que %(username)s.',
    }.get(locale, 'You are logged in as %(username)s.')
    not_logged_in_message = {
        'en': 'You are not logged in.',
        'fr': 'Vous n\'êtes pas connecté.',
    }.get(locale, 'You are not logged in.')

    user = g.get('user')

    return render_template('5-index.html',
                           login_message=login_message,
                           not_logged_in_message=not_logged_in_message,
                           user=user)


if __name__ == '__main__':
    app.run()
