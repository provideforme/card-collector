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

  def __repr__(self):
    return f"Card('{self.id}', '{self.name}')"

  def serialize(self):
    card = {c.name: getattr(self, c.name) for c in self.__table__.columns}
    return card