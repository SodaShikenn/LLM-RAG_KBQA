from flask import render_template, request, session, redirect, url_for, flash
from . import bp


@bp.route('/login', endpoint='login')
def index():
    return render_template('auth/login.html')

