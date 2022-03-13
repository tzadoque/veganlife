from app import db

class Product(db.Model):
  __tablename__ = "products"
  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String(84), nullable=False)
  category = db.Column(db.String(84), nullable=False)
  type = db.Column(db.String(1), nullable=False)
  description = db.Column(db.String(2048), nullable=False)
  picture = db.Column(db.String(256))

  def __str__(self):
    return self.name