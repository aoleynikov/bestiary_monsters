import json
from flask import Flask, Response
from monsters_blueprint import monsters_blueprint
from skills_blueprint import skills_blueprint

app = Flask(__name__)


@app.route('/')
def hello_world():
    return Response('Hello, World', status=200, content_type='text/plain')


app.register_blueprint(monsters_blueprint)
app.register_blueprint(skills_blueprint)

if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0')
