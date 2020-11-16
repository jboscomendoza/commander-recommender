from app import db

class Commander(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    card_id = db.Column(db.String(64), index=True, unique=True)
    card_name = db.Column(db.String(120), index=True)
    url_scryfall = db.Column(db.String(240))
    url_img = db.Column(db.String(240))
    recs_text = db.relationship('RecsText', backref='card_origen', lazy='dynamic')

    def __repr__(self):
        return "<Card name: {}>".format(self.card_name)

class RecsText(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    card_id = db.Column(db.String(64), index=True)
    rec_id = db.Column(db.String(120), db.ForeignKey("commander.card_id"))
    similitud = db.Column(db.Numeric())
    commander = db.relationship('Commander', backref='card_recs')

    def __repr__(self):
        return "<Similitud: {}>".format(self.similitud)
