import os
from flask import Flask, request, jsonify, url_for, make_response
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, User, People, Planets, Favorites
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False

db_url = os.getenv("DATABASE_URL")
if db_url is not None:
    app.config['SQLALCHEMY_DATABASE_URI'] = db_url.replace("postgres://", "postgresql://")
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:////tmp/test.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

@app.route('/people/<int:people_id>', methods=['GET'])
def handle_get_one_person(people_id):
    person = People.query.get(people_id)
    if person:
        return jsonify({
            "id": person.id,
            "name": person.name,
            "description": person.description
        }), 200
    else:
        return jsonify({"error": "Person not found"}), 404

@app.route('/people', methods=['GET'])
def handle_get_all_people():
    people = People.query.all()
    return jsonify([{
        "id": person.id,
        "name": person.name,
        "description": person.description
    } for person in people]), 200

@app.route('/favorites/planets/<int:planets_id>', methods=['POST'])
def add_fav_planet(planets_id):
    data = request.get_json()
    new_Fav_Planet = Favorites(user_id=data["user_id"], planets_id = planets_id)
    db.session.add(new_Fav_Planet)
    db.session.commit()
    return jsonify(new_Fav_Planet.serialize()), 200

@app.route('/planets/<int:planet_id>', methods=['GET'])
def handle_get_one_planet(planet_id):
    planet = Planets.query.get(planet_id)
    if planet:
        return jsonify({
            "id": planet.id,
            "name": planet.name,
            "description": planet.description
        }), 200
    else:
        return jsonify({"error": "Planet not found"}), 404

@app.route('/planets', methods=['GET'])
def handle_get_all_planets():
    planets = Planets.query.all()
    return jsonify([{
        "id": planet.id,
        "name": planet.name,
        "description": planet.description
    } for planet in planets]), 200


@app.route('/user', methods=['GET'])
def get_users():
    users = User.query.all()
    return jsonify([{
        "id": user.id,
        "email": user.email,
    } for user in users]), 200


@app.route('/user/favorites', methods=['GET'])
def get_user_favorites():
    faves= Favorites.query.all()
    all_faves = list(map(lambda x: x.serialize(), faves))
    return jsonify(all_faves)




