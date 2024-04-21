from time import sleep
import deezer
from tunefinder.definitions.Track import Track
from tunefinder import logger

API_SLEEP_SECONDS = 0.2
API_RATE_LIMIT_SLEEP_SECONDS = 5


class Deezer:
    def __init__(self):
        self.client = deezer.Client()

    def track(self, track):
        if track is None:
            return None

        id = track['id'] if 'id' in track else None
        title = track['title'] if 'title' in track else None
        artist = track['artist'].__dict__[
            'name'] if 'artist' in track and 'name' in track['artist'].__dict__ else None
        album = track['album'].__dict__[
            'title'] if 'album' in track and 'title' in track['album'].__dict__ else None
        isrc = track['isrc'] if 'isrc' in track else None
        url = track['link'] if 'link' in track else None

        return Track(
            platform='deezer',
            id=id,
            title=title,
            artist=artist,
            album=album,
            isrc=isrc,
            url=url)

    def playlist(self, playlist):
        return [self.track(item) for item in playlist]

    def get_track(self, uri, retries=0):
        try:
            result = self.client.get_track(uri.split('/')[-1]).__dict__
            sleep(API_SLEEP_SECONDS)
            return result
        except deezer.exceptions.DeezerErrorResponse:
            logger.error(f'Track with URI {uri} not found')
            return None
        except (deezer.exceptions.DeezerForbiddenError, deezer.exceptions.DeezerRetryableHTTPError):
            if (retries < 3):
                logger.warn(f'API rate limit exceeded, retrying in a bit...')
                sleep(API_RATE_LIMIT_SLEEP_SECONDS * (retries + 1))
                return self.get_track(uri, retries + 1)
            logger.error(f'API rate limit exceeded')
            return None

    def get_track_by_isrc(self, isrc, retries=0):
        try:
            result = self.client.request(
                "GET", "track/isrc:" + isrc, resource_type=deezer.Track).__dict__
            try:
                artist = f'{result["artist"].__dict__["name"]} - '
            except KeyError:
                artist = ""
            try:
                title = result["title"]
            except KeyError:
                title = ""
            logger.info(
                f'Track with ISRC {isrc} resolved to {artist}{title}')
            sleep(API_SLEEP_SECONDS)
            return result
        except deezer.exceptions.DeezerErrorResponse:
            logger.error(f'Track with ISRC {isrc} not found')
            return None
        except (deezer.exceptions.DeezerForbiddenError, deezer.exceptions.DeezerRetryableHTTPError):
            if (retries < 3):
                logger.warn(f'API error occurred, retrying in a bit...')
                retries = retries + 1
                sleep(API_RATE_LIMIT_SLEEP_SECONDS * retries)
                return self.get_track_by_isrc(isrc, retries)
            logger.error(f'API error occurred')
            return None

    def get_playlist(self, uri):
        playlist = self.client.get_playlist(
            uri.split('/')[-1]).__dict__['tracks']
        sleep(API_SLEEP_SECONDS)
        tracks = []
        for item in playlist:
            tracks.append(self.get_track(item.__dict__['link']))
        return list(filter(lambda item: item is not None, tracks))

    def get_playlist_by_isrc(self, isrcs):
        length = len(isrcs)
        for i, isrc in enumerate(isrcs):
            logger.progress('Processing track', i + 1, length)
            yield self.get_track_by_isrc(isrc)
