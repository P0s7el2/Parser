from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy import Column, Integer, String


Base = declarative_base()


# orm-классы
class Track(Base):
    __tablename__ = 'tracks'
    id = Column(Integer, primary_key=True)
    artist = Column(String)
    title = Column(String)
    set_id = Column(String, ForeignKey("musicsets.id"))
    musicset = relationship("Musicset", backref='tracks')

    def __init__(self, artist, title, set_id):
        self.artist = artist
        self.title = title
        self.set_id = set_id

    def __repr__(self):
        return "<Track(artist: '%s', title: '%s', set_id: '%s'>" % (self.artist, self.title, self.set_id)


class Musicset(Base):
    __tablename__ = 'musicsets'
    id = Column(Integer, primary_key=True)
    set_title = Column(String)
    set_link = Column(String)
    set_tracks = Column(String)

    def __str__(self):
        return "<Set id - %s>" % self.id

    def __init__(self, id, set_tracks, set_link, set_title):
        self.id = id
        self.set_title = set_title
        self.set_link = set_link
        self.set_tracks = set_tracks

    def __repr__(self):
        return "<Track(id: '%s', set_title: '%s', link: '%s', set_tracks: '%s'>" % (self.id, self.set_title, self.link, self.set_tracks)