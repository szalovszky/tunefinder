import os
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from tunefinder.definitions.Track import Track
from tunefinder import logger


class Spotify:
    def __init__(self):
        if ('SPOTIFY_CLIENT_ID' not in os.environ or 'SPOTIFY_CLIENT_SECRET' not in os.environ):
            raise Exception('Spotify API credentials not found. Please set SPOTIFY_CLIENT_ID and SPOTIFY_CLIENT_SECRET environment variables. See https://github.com/szalovszky/tunefinder#credentials for more information.')
        self.client_id = os.environ['SPOTIFY_CLIENT_ID']
        self.client_secret = os.environ['SPOTIFY_CLIENT_SECRET']
        self.client = spotipy.Spotify(auth_manager=SpotifyClientCredentials(client_id=self.client_id,
                                      client_secret=self.client_secret))

    def track(self, track):
        if track is None:
            return None

        id = track['id'] if 'id' in track else None
        title = track['name'] if 'name' in track else None
        artist = track['artists'][0]['name'] if 'artists' in track and 'name' in track['artists'][0] else None
        album = track['album']['name'] if 'album' in track and 'name' in track['album'] else None
        isrc = track['external_ids']['isrc'] if 'external_ids' in track and 'isrc' in track['external_ids'] else None
        url = track['external_urls']['spotify'] if 'external_urls' in track and 'spotify' in track['external_urls'] else None

        return Track(
            platform='spotify',
            id=id,
            title=title,
            artist=artist,
            album=album,
            isrc=isrc,
            url=url)

    def playlist(self, playlist):
        return [self.track(item) for item in playlist]

    def get_track(self, uri):
        return self.client.track(uri)

    def get_track_by_isrc(self, isrc):
        try:
            result = self.client.search(q=f'isrc:{isrc}', type='track', limit=1)[
                'tracks']['items'][0]
            logger.info(
                f'Track with ISRC {isrc} resolved to {result["artists"][0]["name"]} - {result["name"]}')
            return result
        except IndexError:
            logger.error(f'Track with ISRC {isrc} not found')
            return None

    def get_playlist(self, uri):
        playlist_items = []
        next_page = True
        offset = 0

        while (next_page != False):
            playlist = self.client.playlist_tracks(
                uri, offset=offset)
            playlist_items.extend(playlist['items'])

            if (playlist['next'] == None):
                next_page = False
            else:
                offset += playlist['limit']

        tracks = []
        for item in playlist_items:
            tracks.append(item['track'])
        return tracks

    def get_playlist_by_isrc(self, isrcs):
        length = len(isrcs)
        for i, isrc in enumerate(isrcs):
            logger.progress('Processing track', i + 1, length)
            yield self.get_track_by_isrc(isrc)
