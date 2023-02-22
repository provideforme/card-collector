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