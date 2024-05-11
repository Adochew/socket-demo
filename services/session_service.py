from models.session import Session, Message
from routes import db


class SessionService:
    @staticmethod
    def get_sessions():
        sessions = Session.query.order_by(Session.session_id.desc()).all()
        session_list = []
        for session in sessions:
            session_record = {
                'session_id': session.session_id,
                'session_info': session.session_info,
            }
            session_list.append(session_record)
        return session_list

    @staticmethod
    def add_session(session_info='new session'):
        new_session = Session(session_info=session_info)
        db.session.add(new_session)
        db.session.commit()
        return new_session.session_id

    @staticmethod
    def update_session_info(session_id, new_info):
        session = Session.query.filter_by(session_id=session_id).first()
        if session:
            session.session_info = new_info
            db.session.commit()
        else:
            raise Exception(f'Session with session_id: {session_id} does not exist')

    @staticmethod
    def delete_session(session_id):
        session = Session.query.filter_by(session_id=session_id).first()
        if session:
            for message in session.messages:
                db.session.delete(message)
                # 再删除会话本身
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
