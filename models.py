from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Announcement(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    date = db.Column(db.String(25), nullable=False)
    title = db.Column(db.String(225), nullable=False)
    media = db.Column(db.String(225), nullable=False)

    def __init__(self, date, title, media):
        self.date = date
        self.title = title
        self.media = media
