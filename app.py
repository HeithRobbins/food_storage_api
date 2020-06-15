from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_cors import CORS
from flask_heroku import Heroku
from environs import Env
import os

app = Flask(__name__)
CORS(app)
heroku = Heroku(app)

env = Env()
env.read_env()
DATABASE_URL = env("DATABASE_URL")


basedir = os.path.abspath(os.path.dirname(__file__))
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'app.sqlite')
app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE_URL

db = SQLAlchemy(app)
ma = Marshmallow(app)

class Storage(db.Model):
    __tablename__ = "storage"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=False)
    date = db.Column(db.String(25), unique=False)
    weight = db.Column(db.Integer, unique=False)
    amount = db.Column(db.Integer, unique=False)

    def __init__(self, name, date, weight = 0, amount = 0):
        self.name = name
        self.date = date
        self.weight = weight
        self.amount = amount

class StorageSchema(ma.Schema):
        class Meta:
            fields = ('id', 'name', 'date', 'weight', 'amount')


storage_schema = StorageSchema()
storages_schema = StorageSchema(many=True)

@app.route("/", methods=["GET"])
def home():
  return "<h1>Storage Flask API</h1>"

@app.route('/storage', methods=["POST"])
def add_storage():
    name = request.json['name']
    date = request.json['date']
    weight = request.json['weight']
    amount = request.json['amount']

    new_Storage = Storage(name, date, weight, amount)

    db.session.add(new_Storage)
    db.session.commit()

    storage = Storage.query.get(new_Storage.id)

    return storage_schema.jsonify(storage)


@app.route("/storages", methods=["GET"])
def get_storages():
    all_storages = Storage.query.all()
    result = storages_schema.dump(all_storages)
    return jsonify(result)


@app.route("/storage/<id>", methods=["GET"])
def get_storage(id):
    storage = Storage.query.get(id)
    return storage_schema.jsonify(storage)


@app.route("/storage/<id>", methods=["PATCH"])
def storage_update(id):
    storage = Storage.query.get(id)
    name = request.json['name']
    date = request.json['date']
    weight = request.json['weight']
    amount = request.json['amount']

    storage.name = name
    storage.date = date
    storage.weight = weight
    storage.amount = amount

    db.session.commit()
    return guide_schema.jsonify(guide)


@app.route("/storage/<id>", methods=["DELETE"])
def storage_delete(id):
    storage = Storage.query.get(id)
    db.session.delete(storage)
    db.session.commit()

    return jsonify("Your food storage item was successfully delete")


if __name__ == '__main__':
    app.run(debug=True)