from flask import Flask , request , jsonify
import jwt
import datetime
from functools import wraps
from Models.Users_Requests import usersblp
from Models.Posts_Requests import postsblp

from flask import Flask
from flask_cors import CORS ,cross_origin

app = Flask(__name__)

@app.route('/')
def index():
    return 'Welcome'

CORS(app)


app.register_blueprint(usersblp , url_prefix="/api/users")
app.register_blueprint(postsblp , url_prefix="/api/posts")


app.config['JSON_AS_ASCII'] = False
app.config['SECRET_KEY'] = '654321'


if __name__ == '__main__':
    # app.run(debug=False,host='0.0.0.0')
    app.run(debug=True)
