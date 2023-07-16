from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Playlist(db.Model):
    """Playlist."""

    __tablename__ = 'playlists'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)

    playlist_songs = db.relationship('PlaylistSong', back_populates='playlist')

    @property
    def songs(self):
        return [ps.song for ps in self.playlist_songs]


class Song(db.Model):
    """Song."""

    __tablename__ = 'songs'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80), nullable=False)
    artist = db.Column(db.String(80), nullable=False)

    playlist_songs = db.relationship('PlaylistSong', back_populates='song')



class PlaylistSong(db.Model):
    """Mapping of a playlist to a song."""

    __tablename__ = 'playlist_songs'

    id = db.Column(db.Integer, primary_key=True)
    song_id = db.Column(db.Integer, db.ForeignKey('songs.id'))
    playlist_id = db.Column(db.Integer, db.ForeignKey('playlists.id'))

    song = db.relationship('Song', back_populates='playlist_songs', lazy='joined')
    playlist = db.relationship('Playlist', back_populates='playlist_songs', lazy='joined')



