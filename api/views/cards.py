from flask import Blueprint, jsonify, request
from api.middleware import login_required, read_token

from api.models.db import db
from api.models.card import Card

cards = Blueprint('cards', 'cards')

@cards.route('/', methods=["POST"])
@login_required
def create():
  data = request.get_json()
  profile = read_token(request)
  data["profile_id"] = profile["id"]
  card = Card(**data)
  db.session.add(card)
  db.session.commit()
  return jsonify(card.serialize()), 201

@cards.route('/', methods=["GET"])
def index():
  cards = Card.query.all()
  return jsonify([card.serialize() for card in cards]), 200

@cards.route('/<id>', methods=["GET"])
def show(id):
  card = Card.query.filter_by(id=id).first()
  card_data = card.serialize()
  return jsonify(card=card_data), 200

@cards.route('/<id>', methods=["PUT"])
@login_required
def update(id):
  data = request.get_json()
  profile = read_token(request)
  card = Card.query.filter_by(id=id).first()

  if card.profile_id != profile["id"]:
    return 'Forbidden', 403

  for key in data:
    setattr(card, key, data[key])

  db.session.commit()
  return jsonify(card.serialize()), 200

@cards.route('/<id>', methods=["DELETE"])
@login_required
def delete(id):
  profile = read_token(request)
  card = Card.query.filter_by(id=id).first()

  if card.profile_id != profile["id"]:
    return 'Forbidden', 403

  db.session.delete(card)
  db.session.commit()
  return jsonify(message="Success"), 200