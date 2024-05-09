class Session:
    def __init__(self, session_id):
        self.session_id = session_id
        self.history = []

    def add_message(self, role, content):
        self.history.append({'role': role, 'content': content})

    def get_history(self):
        return self.history

    def get_session_id(self):
        return self.session_id
