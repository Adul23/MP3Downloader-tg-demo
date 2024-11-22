from config import db

class Contact(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), unique=False, nullable=False)
    url = db.Column(db.String(250), unique=False, nullable=False)

    def to_json(self):
        return {
            "id": self.id,
            "name": self.name,
            "url": self.url 
        }
