from routes import app
from flask import render_template

@app.route('/')
@app.route('/index.html')
def home_page():
    return render_template('index.html')