from flask import Flask, render_template, request, redirect, url_for
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

app = Flask(__name__)

# Set your Spotify API credentials
client_id = "30620e4113c7459bbe66e0b10854a983"
client_secret = "18256ca6b0b94844a41e13e06201e4a6"

client_credentials_manager = SpotifyClientCredentials(
    client_id=client_id, client_secret=client_secret)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/search', methods=['POST'])
def search():
    artist = request.form.get('artist')
    song = request.form.get('song')

    # Constructing the search query based on input
    query = ''
    if artist:
        query += 'artist:' + artist
    if song:
        # If there is already a part of the query (artist), add a space
        if query:
            query += ' '
        query += 'track:' + song

    # Perform the search if there's a query, else redirect to home
    if query:
        results = sp.search(q=query, type='track')
        track = results['tracks']['items'][0] if results['tracks']['items'] else None

        if track:
            features = sp.audio_features(track['id'])[0]
            return render_template('results.html', track=track, features=features)
        else:
            return render_template('no_results.html')
    else:
        return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True)
