from flask import Flask, session, request, make_response, jsonify
from flask_restful import Api, Resource, abort, reqparse
import jwt
import datetime
from functools import wraps
import json

from firebase import *

# flask and api initalization
app = Flask(__name__)
api = Api(app)
# token key
app.config["SECRET_KEY"] = "thisisthesecretkey"

# decoratordiki - protects the access to the enpoint by validating the token
def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        #token = request.args.get("token") #http://127.0.0.1:5000/protected?token=...
        token = session.get("token")
        if not token:
            return jsonify({"message" : "Token is missing!"}), 403
        try: 
            data = jwt.decode(token, app.config["SECRET_KEY"], algorithms=["HS256"])
        except:
            return jsonify({"message" : "Token is invalid!"}), 403
        
        return f(*args, **kwargs)
    
    return decorated

# endpoint /unprotected - returns movies that are available to all users
@app.route("/unprotected")
def unprotected():
    movies_unprotected = {}
    for key in movies:
        if(movies[key]["protected"] == "False"):
            movies_unprotected[key] = movies[key]
    
    return jsonify({"message": "Anyone can view this", "movies": movies_unprotected})

# endpoint /protected - returns all movies
@app.route("/protected")
@token_required # dekorator: protected = token_required(protected)
def protected():
    return jsonify({"message": "This is only available to people with valid tokens", "movies": movies})

# endpoint /login - user authorization
@app.route("/login")
def login():
    auth = request.authorization

    if auth and auth.username == "user" and auth.password == "pass":
        token = jwt.encode({"user" : auth.username, "exp" : datetime.datetime.utcnow() + datetime.timedelta(minutes=15)}, app.config["SECRET_KEY"], algorithm="HS256")
        decoded = token.decode("UTF-8")
        session["token"] = decoded
        print("Token = " + str(session["token"]))
        return jsonify({"token" : decoded})

    return make_response("Could not verify!", 401, {"WWW-Authenticate" : "Basic realm='Login Required'"})

# setting required movie arguments to add valid movies
movie_put_args = reqparse.RequestParser()
movie_put_args.add_argument("title", type=str, help="Missing the title", required=True)
movie_put_args.add_argument("year", type=str, help="Missing the year", required=True)
movie_put_args.add_argument("rating", type=str, help="Missing the rating", required=True)
movie_put_args.add_argument("actors", type=str, help="Missing the actors", required=True)
movie_put_args.add_argument("protected", type=str, help="Missing the protected", required=True)

# getting dictionary of movies from database
movies = firebase_get()

def abort_if_movie_id_doesnt_exist(movie_id):
    if movie_id not in movies:
        abort(404, message="Could not find movie with ID = " + movie_id + "... aborting")

def abort_if_movie_exists(movie_id):
    if movie_id in movies:
        abort(409, message="Movie already exists with that ID... aborting")

# class describes funcionality of requests
class MovieRequests(Resource):
    def get(self, movie_id):
        abort_if_movie_id_doesnt_exist(movie_id)
        return movies[movie_id]

    def put(self, movie_id):
        abort_if_movie_exists(movie_id)
        args = movie_put_args.parse_args()
        movies[movie_id] = args
        firebase_push(movie_id, args)
        return movies[movie_id], 201
        
    def delete(self, movie_id):
        abort_if_movie_id_doesnt_exist(movie_id)
        firebase_delete(movie_id)
        del movies[movie_id]
        return {}, 204

api.add_resource(MovieRequests, "/movie/<int:movie_id>")

def database_auth():
    print("Firebase authentication: ")
    firebase_login()

# flask starts here
if __name__ == "__main__":
    #database_auth()
    app.run(debug=True)