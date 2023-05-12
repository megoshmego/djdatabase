"""Forms for playlist app."""

from wtforms import SelectField, StringField, validators, SubmitField
from flask_wtf import FlaskForm


class PlaylistForm(FlaskForm):
    """Form for adding playlists."""
    playlist_name = StringField("Playlist Name", validators=[validators.DataRequired()])
    submit = SubmitField("Submit")
    


class SongForm(FlaskForm):
    """Form for adding songs."""
    title = StringField("Song Title", validators=[validators.DataRequired()])
    artist = StringField("Song Artist", validators=[validators.DataRequired()])
    submit = SubmitField("Submit")
   



# DO NOT MODIFY THIS FORM - EVERYTHING YOU NEED IS HERE
class NewSongForPlaylistForm(FlaskForm):
    """Form for adding a song to playlist."""

    song = SelectField('Song To Add', coerce=int)
    submit = SubmitField("Submit")
    
    