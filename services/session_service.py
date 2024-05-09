from models.session import Session, Message
from routes import db


class SessionService:
    @staticmethod
    def add_session(session_id):
        if session_id:
            new_session = Session(session_id=session_id)
            db.session.add(new_session)
            db.session.commit()

    @staticmethod
    def delete_session(session_id):
        session = Session.query.filter_by(session_id=session_id).first()
        if session:
            db.session.delete(session)
            db.session.commit()

    @staticmethod
    def add_message(session_id, role, content):
        session = Session.query.filter_by(session_id=session_id).first()
        if not session:
            session = Session(session_id=session_id)
            db.session.add(session)
        message = Message(session_id=session_id, role=role, content=content)
        db.session.add(message)
        db.session.commit()

    @staticmethod
    def get_history(session_id):
        session = Session.query.filter_by(session_id=session_id).first()
        if session:
            history = [
                {'role': msg.role,
                 'content': msg.content,
                 'timestamp': msg.timestamp.strftime('%Y-%m-%d %H:%M:%S')}
                for msg in session.messages
            ]
            return history
        else:
            raise Exception(f'session_id: {session_id} 不存在')