from flask import render_template
from . import main
from ..models import User
from os import abort


@main.route('/')
def index():
    return render_template('index.html')


@main.route('/user/<username>')
def user(username):
    users = User.query.filter_by(username=username).first()
    if users is None:
        abort(404)
    return render_template('user.html', user=users)
