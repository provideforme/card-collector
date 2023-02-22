from flask import Blueprint, jsonify, request
from api.middleware import login_required, read_token

from api.models.db import db
from api.models.set import Set

sets = Blueprint('sets', 'sets')

@sets.route('/', methods=["POST"])
@login_required
def create():
  data = request.get_json()
  profile = read_token(request)
  data["profile_id"] = profile["id"]

  set = Set(**data)
  db.session.add(set)
  db.session.commit()
  return jsonify(set.serialize()), 201

@sets.route('/', methods=["GET"])
def index():
  sets = Set.query.all()
  return jsonify([set.serialize() for set in sets]), 201

@sets.route('/<id>', methods=["GET"])
def show(id):
  set = Set.query.filter_by(id=id).first()
  return jsonify(set.serialize()), 200

