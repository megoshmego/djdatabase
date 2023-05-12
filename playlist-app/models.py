from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Playlist(db.Model):
    """Playlist."""

    __tablename__ = 'playlist'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)

    # This is the "many" side of a many-to-many relationship with Song via the PlaylistSong association table.
    songs = db.relationship('PlaylistSong', backref='playlist', cascade="all, delete")


class Song(db.Model):
    """Song."""

    __tablename__ = 'songs'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80), nullable=False)
    artist = db.Column(db.String(80), nullable=False)

    playlists = db.relationship('Playlist', secondary='playlist_song', backref='songs')



class PlaylistSong(db.Model):
    """Mapping of a playlist to a song."""

    __tablename__ = 'playlist_song'

    id = db.Column(db.Integer, primary_key=True)
    song_id = db.Column(db.Integer, db.ForeignKey('song.id'))
    playlist_id = db.Column(db.Integer, db.ForeignKey('playlist.id'))


# DO NOT MODIFY THIS FUNCTION
def connect_db(app):
    """Connect to database."""

    db.app = app
    db.init_app(app)
