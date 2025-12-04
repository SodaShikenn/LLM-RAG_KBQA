from flask import render_template, request, session, redirect, url_for, flash
from . import bp
from .services import validate_user


@bp.route('/login', endpoint='login', methods=['GET','POST'])

def index():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        if not email or '@' not in email:
            flash('Please enter valid email address', 'error')
        elif not password:
            flash('Please enter your passsword', 'error')

        elif validate_user(email, password):
            session['user'] = email  # Store email in session to maintain login state
            return redirect(url_for('index'))  # Redirect to homepage after successful login
        else:
            flash('Incorrect email or password', 'error')
    
    if session.get('user'):
        return redirect(url_for('index'))

    return render_template('auth/login.html')

@bp.route('/logout', endpoint='logout')
def logout():
    session.pop('user', None)  # Remove session data
    return redirect(url_for('auth.login'))  # Redirect to login page