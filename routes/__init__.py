from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__,
            template_folder='../templates',
            static_folder='../assets',
            static_url_path='/assets')
app.secret_key = 'csu.edu.cn'

# 配置数据库连接
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqldb://root:123456@localhost/socket_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # 关闭对模型修改的监控

# 初始化 SQLAlchemy
db = SQLAlchemy(app)

from routes import user_routes, chat_routes
