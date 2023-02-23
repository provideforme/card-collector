from flask import Flask
from flask_cors import CORS
from flask_migrate import Migrate
from api.models.db import db
from config import Config

# ============ Import Models ============
from api.models.trading import Trading
from api.models.set import Set
from api.models.card import Card
from api.models.user import User
from api.models.profile import Profile

# ============ Import Views ============
from api.views.sets import sets
from api.views.cards import cards
from api.views.auth import auth

cors = CORS()
migrate = Migrate() 
list = ['GET', 'HEAD', 'POST', 'OPTIONS', 'PUT', 'PATCH', 'DELETE', 'LINK']

def create_app(config):
  app = Flask(__name__)
  app.config.from_object(config)

  db.init_app(app)
  migrate.init_app(app, db)
  cors.init_app(app, supports_credentials=True, methods=list)

  # ============ Register Blueprints ============
  app.register_blueprint(sets, url_prefix='/api/sets')
  app.register_blueprint(cards, url_prefix='/api/cards')
  app.register_blueprint(auth, url_prefix='/api/auth') 

  return app

app = create_app(Config)