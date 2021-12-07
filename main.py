from flask import Flask

from user import user
from ticket import ticket
from event import event

app = Flask(__name__)
app.register_blueprint(user)
app.register_blueprint(ticket)
app.register_blueprint(event)

@app.route('/api/v1/hello-world-8')
def hello_world():
    return 'Hello World 8'