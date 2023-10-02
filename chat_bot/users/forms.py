from flask_wtf import FlaskForm
from wtforms import ValidationError, StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo
from chat_bot.models import User

class LoginForm(FlaskForm):
    email = StringField('メールアドレス', validators=[DataRequired(), Email(message='正しいメールアドレスの形式で入力してください')])
    password = PasswordField('パスワード', validators=[DataRequired()])
    submit = SubmitField('ログイン')

class RegistrationUserForm(FlaskForm):
    username = StringField('ユーザー名', validators=[DataRequired()])
    email = StringField('メールアドレス', validators=[DataRequired(), Email(message='正しいメールアドレスの形式で入力してください'), EqualTo('email_confirm',message='メールアドレスが一致しません')])
    email_confirm = StringField('メールアドレス（確認）', validators=[DataRequired(), Email(message='正しいメールアドレスの形式で入力してください')])
    password = PasswordField('パスワード', validators=[DataRequired(), EqualTo('password_confirm', message='パスワードが一致しません')])
    password_confirm = PasswordField('パスワード（確認）', validators=[DataRequired()])
    submit = SubmitField('登録')

    #ユーザー名重複チェック
    def validate_username(self, field):
        if User.query.filter_by(username = field.data).first():
            raise ValidationError('入力されたユーザー名は既に登録されています')

    #メールアドレス重複チェック
    def validate_email(self, field):
        if User.query.filter_by(email = field.data).first():
            raise ValidationError('入力されたメールアドレスは既に登録されています')

class UpdateUserForm(FlaskForm):
    username = StringField('ユーザー名', validators=[DataRequired()])
    email = StringField('メールアドレス', validators=[DataRequired(), Email(message='正しいメールアドレスの形式で入力してください'), EqualTo('email_confirm',message='メールアドレスが一致しません')])
    email_confirm = StringField('メールアドレス（確認）', validators=[DataRequired(), Email(message='正しいメールアドレスの形式で入力してください')])
    password = PasswordField('パスワード', validators=[EqualTo('password_confirm', message='パスワードが一致しません')])
    password_confirm = PasswordField('パスワード（確認）')
    submit = SubmitField('更新')

    def __init__(self, user_id, *args, **kwargs):
        super(UpdateUserForm, self).__init__(*args, **kwargs)
        self.id = user_id
    
    #ユーザー名重複チェック
    def validate_username(self, field):
        if User.query.filter(User.id != self.id).filter_by(username = field.data).first():
            raise ValidationError('入力されたユーザー名は既に登録されています')

    #メールアドレス重複チェック
    def validate_email(self, field):
        if User.query.filter(User.id != self.id).filter_by(email = field.data).first():
            raise ValidationError('入力されたメールアドレスは既に登録されています')