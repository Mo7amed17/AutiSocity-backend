from flask import Flask , request , jsonify , send_from_directory
import jwt
import datetime
from functools import wraps
from Models.Users_Requests import usersblp
from Models.Posts_Requests import postsblp

from flask_cors import CORS ,cross_origin

app = Flask(__name__)

@app.route('/')
def index():
    return send_from_directory('../', 'public_python\uploads\avatars\2024-04-09_04.55.59.664066Untitled.jpg')

CORS(app)

app.register_blueprint(usersblp , url_prefix="/api/users")
app.register_blueprint(postsblp , url_prefix="/api/posts")


app.config['JSON_AS_ASCII'] = False
app.config['SECRET_KEY'] = '654321'


if __name__ == '__main__':
    # app.run(debug=False,host='0.0.0.0')
    app.run()
