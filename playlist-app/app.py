from flask import Flask, redirect, render_template
from flask_debugtoolbar import DebugToolbarExtension

from models import db, connect_db, Playlist, Song, PlaylistSong
from forms import NewSongForPlaylistForm, SongForm, PlaylistForm

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://megan:mego@localhost/databasedj'

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

connect_db(app)
db.create_all()

app.config['SECRET_KEY'] = "I'LL NEVER TELL!!"

# Having the Debug Toolbar show redirects explicitly is often useful;
# however, if you want to turn it off, you can uncomment this line:
#
# app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

debug = DebugToolbarExtension(app)


@app.route("/")
def root():
    """Homepage: redirect to /playlists."""

    return redirect("/playlists")


##############################################################################
# Playlist routes


@app.route("/playlists")
def show_all_playlists():
    """Return a list of playlists."""

    playlists = Playlist.query.all()
    return render_template("playlists.html", playlists=playlists)


@app.route("/playlists/<int:playlist_id>")
def show_playlist(playlist_id):
    """Show detail on specific playlist."""
   
    playlist = Playlist.query.get_or_404(playlist_id)
    return render_template('playlist.html', playlist=playlist)


@app.route("/playlists/add", methods=["GET", "POST"])
def add_playlist():
    form = PlaylistForm()
    """Handle add-playlist form:

    - if form not filled out or invalid: show form
    - if valid: add playlist to SQLA and redirect to list-of-playlists
    """
    if form.validate_on_submit():
        new_playlist = Playlist(name=form.playlist_name.data) 
        db.session.add(new_playlist)
        db.session.commit()
        return redirect("/playlists")

    return render_template('new_playlist.html', form=form)

    
   
        

##############################################################################
# Song routes


@app.route("/songs")
def show_all_songs():
    """Show list of songs."""

    songs = Song.query.all()
    return render_template("songs.html", songs=songs)


@app.route("/songs/<int:song_id>")
def show_song(song_id):
    """return a specific song"""
    song = Song.query.get_or_404(song_id)
    return render_template('song.html', song=song)



@app.route("/songs/add", methods=["GET", "POST"])
def add_song():
    form=SongForm()
    
    if form.validate_on_submit():
        song_title=form.title.data
        song_artist=form.artist.data
        new_song=Song(title=song_title, artist=song_artist)
        db.session.add(new_song)    
        db.session.commit()    
        return redirect("/songs")

    return render_template("new_song.html", form=form)



@app.route("/playlists/<int:playlist_id>/add-song", methods=["GET", "POST"])
def add_song_to_playlist(playlist_id):
    """Add a playlist and redirect to list."""

    playlist = Playlist.query.get_or_404(playlist_id)
    form = NewSongForPlaylistForm()

    # Restrict form to songs not already on this playlist
    curr_on_playlist = [song.id for song in playlist.songs]  # Assuming 'songs' is a relationship in Playlist model
    eligible_songs = Song.query.filter(Song.id.notin_(curr_on_playlist)).all()  # Assuming Song model exists
    form.song.choices = [(s.id, s.title) for s in eligible_songs]  # Assuming 'title' is a field in Song model

    if form.validate_on_submit():
        # get song from form data
        song = Song.query.get_or_404(form.song.data)
        # add song to playlist's songs
        playlist.songs.append(song)
        # commit the changes
        db.session.commit()

        return redirect(f"/playlists/{playlist_id}")

    return render_template("add_song_to_playlist.html",
                             playlist=playlist,
                             form=form)

