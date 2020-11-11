#from app import db
#from flask_sqlalchemy import SQLAlchemy
#from app import db

class Commander(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    card_id = db.Column(db.String(64), index=True, unique=True)
    card_name = db.Column(db.String(120), index=True, unique=True)
    url_scryfall = db.Column(db.String(180), unique=True)
    url_img = db.Column(db.String(180), unique=True)
    #recs_text = db.relationship('RecsText', backref='card_origen', lazy='dynamic')

    def __repr__(self):
        return "<Card name: {}>".format(self.card_name)

class RecsText(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    card_id = db.Column(db.String(64), index=True, unique=True)
    rec_id = db.Column(db.String(120), db.ForeignKey("Commander.card_id"))
    similitud = db.Column(db.Numeric())

    def __repr__(self):
        return "<Similitud: {}>".format(self.sim)