from datetime import datetime
from api.models.db import db

class Association(db.Model):
  __tablename__ = 'associations'
  id = db.Column(db.Integer, primary_key=True)
  card_id = db.Column(db.Integer, db.ForeignKey('cards.id', ondelete='cascade'))
  set_id = db.Column(db.Integer, db.ForeignKey('sets.id', ondelete='cascade'))

class Set(db.Model):
  __tablename__ = 'sets'
  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String(100))
  series = db.Column(db.String(100))
  year = db.Column(db.Integer)
  created_at = db.Column(db.DateTime, default=datetime.utcnow)
  profile_id = db.Column(db.Integer, db.ForeignKey('profiles.id'))

  def __repr__(self):
    return f"Set('{self.id}', '{self.name}'"

  def serialize(self):
    set = {c.name: getattr(self, c.name) for c in self.__table__.columns}
    return set