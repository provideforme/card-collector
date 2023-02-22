from datetime import datetime
from api.models.db import db

class Set(db.Model):
  __tablename__ = 'Sets'
  id = db.Column(db.Integer, primary_key=True)
  brand = db.Column(db.String(100))
  series = db.Column(db.String(100))
  year = db.Column(db.Integer)
  created_at = db.Column(db.DateTime, default=datetime.utcnow)
  profile_id = db.Column(db.Integer, db.ForeignKey('profiles.id'))

  def __repr__(self):
    return f"Set('{self.id}', '{self.brand}'"

  def serialize(self):
    set = {c.brand: getattr(self, c.name) for c in self.__table__.columns}
    return set