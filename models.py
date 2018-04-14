from parser_flask_api import db


class Musicset(db.Model):
    __tablename__ = 'musicsets'
    id = db.Column(db.Integer, primary_key=True)
    set_title = db.Column(db.String)
    set_link = db.Column(db.String)
    set_tracks = db.Column(db.String)

    def to_dict(self):
        return {
            'id': self.id,
            'set_title:': self.set_title,
            'link:': self.set_link,
            'set_tracks:': self.set_tracks
        }



class Track(db.Model):
    __tablename__ = 'tracks'
    id = db.Column(db.Integer, primary_key=True)
    artist = db.Column(db.String)
    title = db.Column(db.String)
    set_id = db.Column(db.String, db.ForeignKey("musicsets.id"))

    musicset = db.relationship(Musicset, backref='tracks')

    def to_dict(self):
        return {
            'id': self.id,
            'artist:': self.artist,
            'title:': self.title,
            'set_id:': self.set_id
        }
