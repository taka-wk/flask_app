import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager

app = Flask(__name__)

app.config['SECRET_KEY'] = 'mysecretkey'

#DB
basedir = os.path.abspath(os.path.dirname(__file__))
#DBのパス指定(OS、環境に依存しない)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'data.sqlite')
#DB変更履歴は保存しない
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
#DBオブジェクト作成
db = SQLAlchemy(app)
Migrate(app,db)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'users.login'

def localize_callback(*args, **kwargs):
    return 'このページにアクセスするにはログインが必要です'
login_manager.localize_callback = localize_callback

from sqlalchemy.engine import Engine
from sqlalchemy import event

@event.listens_for(Engine, "connect")
def set_sqlite_pragma(dbapi_connection, connection_record):
    cursor = dbapi_connection.cursor()
    cursor.execute("PRAGMA foreign_key=ON")
    cursor.close()

from chat_bot.users.views import users
from chat_bot.error_pages.handlers import error_pages

app.register_blueprint(users)
app.register_blueprint(error_pages)