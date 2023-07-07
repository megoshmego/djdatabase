from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Playlist(db.Model):
    """Playlist."""

    __tablename__ = 'playlists'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)

    songs = db.relationship('PlaylistSong', back_populates='playlist')


class Song(db.Model):
    """Song."""

    __tablename__ = 'songs'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80), nullable=False)
    artist = db.Column(db.String(80), nullable=False)

    playlists = db.relationship('PlaylistSong', back_populates='song')


class PlaylistSong(db.Model):
    """Mapping of a playlist to a song."""

    __tablename__ = 'playlist_songs'

    id = db.Column(db.Integer, primary_key=True)
    song_id = db.Column(db.Integer, db.ForeignKey('songs.id'))
    playlist_id = db.Column(db.Integer, db.ForeignKey('playlists.id'))

    song = db.relationship('Song', back_populates='playlists')
    playlist = db.relationship('Playlist', back_populates='songs')
