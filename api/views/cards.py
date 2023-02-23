from flask import Blueprint, jsonify, request
from api.middleware import login_required, read_token

from api.models.db import db
from api.models.card import Card
from api.models.trades import Trade
from api.models.set import Set
from api.models.set import Association

cards = Blueprint('cards', 'cards')

@cards.route('/<card_id>/sets/<set_id>', methods=["LINK"])
@login_required
def assoc_set(card_id, set_id):
  data = { "card_id": card_id, "set_id": set_id }

  profile = read_token(request)
  card = Card.query.filter_by(id=card_id).first()

  if card.profile_id != profile["id"]:
    return 'Forbidden', 403

  assoc = Association(**data)
  db.session.add(assoc)
  db.session.commit()

  card = Card.query.filter_by(id=card_id).first()
  return jsonify(card.serialize()), 201

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
  card_data["traded"] = card.traded()
  sets = Set.query.filter(Set.id.notin_([set.id for set in card.sets])).all()
  sets=[set.serialize() for set in sets]
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

@cards.route('/<id>/trades', methods=["POST"])
@login_required
def add_trade(id):
  data = request.get_json()
  data["card_id"] = id

  profile = read_token(request)
  card = Card.query.filter_by(id=id).first()

  if card.profile_id != profile["id"]:
    return 'Forbidden', 403

  trade = Trade(**data)

  db.session.add(trade)
  db.session.commit()

  card_data = card.serialize()
  card_data["traded"] = card.traded()

  return jsonify(card_data), 201

...
@cards.errorhandler(Exception)          
def basic_error(err):
  return jsonify(err=str(err)), 500
...