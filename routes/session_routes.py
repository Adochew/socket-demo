from routes import app
from flask import render_template, jsonify, session
from services.session_service import SessionService


@app.route('/sessions', methods=['GET'])
def get_sessions():
    return jsonify(SessionService.get_sessions())


@app.route('/session', methods=['POST'])
def new_session():
    session_id = SessionService.add_session()
    session['current_session_id'] = session_id
    return {"session_id": session_id}, 200


@app.route('/session/<session_id>', methods=['GET'])
def get_session(session_id):
    session['current_session_id'] = session_id
    return jsonify(SessionService.get_history(session_id))


@app.route('/session/<session_id>/<session_info>', methods=['PUT'])
def update_session(session_id, session_info):
    SessionService.update_session_info(session_id, session_info)
    return {"status": "Data received"}, 200


@app.route('/session/<session_id>', methods=['DELETE'])
def delete_session(session_id):
    SessionService.delete_session(session_id)
    return {"status": "Data received"}, 200
