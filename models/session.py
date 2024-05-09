from routes import db


# 定义模型
class Session(db.Model):
    __tablename__ = 'sessions'
    session_id = db.Column(db.String(255), primary_key=True)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    messages = db.relationship('Message', order_by="Message.id", backref='session', lazy=True)


class Message(db.Model):
    __tablename__ = 'messages'
    id = db.Column(db.Integer, primary_key=True)
    session_id = db.Column(db.String(255), db.ForeignKey('sessions.session_id'))
    role = db.Column(db.String(255))
    content = db.Column(db.Text)
    timestamp = db.Column(db.DateTime, default=db.func.current_timestamp())
