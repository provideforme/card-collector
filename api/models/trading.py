from datetime import datetime
from api.models.db import db

class Trading(db.Model):
  __tablename__='trades'
  id = db.Column(db.Integer, primary_key=True)
  trader = db.Column('trader', db.Enum('Shop', 'Individual', name='original_owner'))
  date = db.Column(db.DateTime, default=datetime.now(tz=None))
  created_at = db.Column(db.DateTime, default=datetime.now(tz=None))
  card_id = db.Column(db.Integer, db.ForeignKey('cats.id'))

  def __repr__(self):
    return f"Trading('{self.id}', '{self.trader}'"

  def serialize(self):
    return {
      "id": self.id,
      "trader": self.trader,
      "card_id": self.card_id,
      "date": self.date.strftime('%Y-%m-%d'),
    }
  
  def is_recent_meal(self):
    if self.date.strftime('%Y-%m_%d') == datetime.now(tz=None).strftime('%Y-%m-%d'):
      return True