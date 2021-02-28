from app import app
from flask import render_template, redirect, url_for, flash
from flask_login import current_user, login_user, logout_user


@app.route('/')
def index():
    return redirect(url_for('api_v1.index'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    else:
        return {'1': '1'}


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/me')
def api_me():
    return current_user
