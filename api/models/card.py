from datetime import datetime
from api.models.db import db

class Card(db.Model):
  __tablename__ = 'cards'
  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String(100))
  sport = db.Column(db.String(100))
  description = db.Column(db.String(250))
  age = db.Column(db.Integer)
  created_at = db.Column(db.DateTime, default=datetime.utcnow)
  profile_id = db.Column(db.Integer, db.ForeignKey('profiles.id'))

  trades = db.relationship("Trades", cascade='all')

  def __repr__(self):
    return f"Card('{self.id}', '{self.name}')"

  def serialize(self):
    card = {c.name: getattr(self, c.name) for c in self.__table__.columns}
    trades = [trade.serialize() for trade in self.trades]
    card['trades'] = trades
    return card

  def traded(self):
    if len([f for f in self.trades if f.is_recent_trade() == True]) >= 3:
      return True
    else:
      return False