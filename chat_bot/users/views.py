from flask import render_template, url_for, redirect, session, flash, request
from flask_login import login_user, logout_user, login_required
from chat_bot import db
from chat_bot.models import User
from chat_bot.users.forms import RegistrationUserForm, UpdateUserForm, LoginForm
from flask import Blueprint

users = Blueprint('users', __name__)

#ログイン
@users.route('/login',methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if (user is not None) and (user.check_password(form.password.data)):
            login_user(user)
            next = request.args.get('next')
            if next == None or not next[0] == '/':
                next = url_for('users.top')
            return redirect(next)
        else:
            flash('該当のユーザーは存在しません')
    return render_template('users/login.html', form = form )

#ログアウト
@users.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('users.login'))

# @app.route('/user_maintenance')
# def user_maintenance():
#     return render_template('user_maintenance.html')


#アカウント登録
@users.route("/register", methods=['GET', 'POST'])
def register_user():
    form = RegistrationUserForm()
    #「登録」ボタンが押下された場合
    if form.validate_on_submit():
        # session['username'] = form.email.data
        # session['email'] = form.email.data
        # session['password'] = form.email.data
        user = User(username=form.username.data, email=form.email.data, password=form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('ユーザーが登録されました')
        return redirect(url_for('users.logout'))
    #「アカウント登録はこちら」リンクが押下された場合
    return render_template('users/register.html', form = form)

#アカウント情報更新
@users.route('/<int:user_id>/account', methods=['GET', 'POST'])
@login_required
def update_user(user_id):
    user = User.query.get_or_404(user_id)
    form = UpdateUserForm(user_id)
    #「更新」ボタンが押下された場合
    if form.validate_on_submit():
        user.username = form.username.data
        user.email = form.email.data
        #パスワードが入力されている場合
        if form.password.data:
            user.password = form.password.data
        db.session.commit()
        flash('ユーザー情報が更新されました')
        return redirect(url_for('users.top'))
    #「アカウント情報」ボタンが押下された場合
    elif request.method == 'GET':
        form.username.data = user.username
        form.email.data = user.email
    return render_template('users/account.html', form = form )

#アカウント削除
@users.route('/<int:user_id>/delete', methods=['GET', 'POST'])
@login_required
def delete_user(user_id):
    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()
    flash('ユーザーが削除されました')
    return redirect(url_for('users.logout'))

#ログイン画面へ遷移
@users.route("/")
def index():
    return redirect(url_for('users.logout'))

# #トップページ
@users.route("/top")
@login_required
def top():
    return render_template('top.html')