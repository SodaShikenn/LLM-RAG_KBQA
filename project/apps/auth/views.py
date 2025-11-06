from flask import render_template, request, session, redirect, url_for, flash
from . import bp
from .services import validate_user


@bp.route('/login', endpoint='login', methods=['GET','POST'])

def index():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        if validate_user(email, password):
            session['user'] = email  # 记录邮箱作为session，保持登录状态，不清楚的可以查GPT
            return redirect(url_for('index'))  # 登录成功后重定向到首页
        else:
            flash('邮箱或密码错误。', 'error')
    
    return render_template('auth/login.html')
