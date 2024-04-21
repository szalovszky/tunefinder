from datetime import datetime
from tunefinder import platforms
from tunefinder.definitions.Destination import Destination
from tunefinder.definitions.Result import Result
from tunefinder.definitions.Source import Source
from tunefinder.definitions.Url import Url
from tunefinder import logger


class Tunefinder:
    def __init__(self, args=None):
        self.start_time = datetime.now()
        self.args = args

        self.source = Source(id=platforms.get_id_by_url(
            args.source), url=Url(args.source))
        self.destination = Destination(id=args.destination)

        logger.info(
            f'{self.source.id.capitalize()} -> {self.destination.id.capitalize()}')

    async def main(self):
        self.source.resolver = platforms.get(self.source.id)
        self.destination.resolver = platforms.get(self.destination.id)
        result = await self.get(self.source.url)
        logger.info(f'Execution time: {datetime.now() - self.start_time}')
        return Result(source=self.source, destination=self.destination, result=result)

    async def get(self, url: Url):
        match url.scheme:
            case 'isrc':
                return [self.get_track_by_isrc(url.hostname)]
            case 'spotify':
                uri_type = url.str.split(':')[1]
                match uri_type:
                    case 'track':
                        return [await self.get_track(url.str)]
                    case 'playlist':
                        return self.get_playlist(url.str)
                    case _:
                        raise NotImplementedError(
                            'Unsupported Spotify URI type')
            case 'http' | 'https':
                if ('track' in url.path):
                    return [await self.get_track(url.str)]
                elif ('playlist' in url.path):
                    return self.get_playlist(url.str)
            case _:
                raise NotImplementedError('Unsupported URL scheme')

    async def get_track(self, id):
        if (self.source.id == self.destination.id):
            logger.warn('Source and destination are the same')
            return self.destination.resolver.track(self.destination.resolver.get_track(id))

        match self.source.id:
            case 'deezer':
                return self.get_track_by_isrc(self.source.resolver.get_track(id)['isrc'])
            case 'spotify':
                return self.get_track_by_isrc(self.source.resolver.get_track(id)['external_ids']['isrc'])
            case 'shazam':
                return self.get_track_by_isrc((await self.source.resolver.get_track(id))['isrc'])
            case _:
                raise NotImplementedError(
                    f'Source type {self.source.id} not supported')

    def get_playlist(self, id):
        if (self.source.id == self.destination.id):
            logger.warn('Source and destination are the same')
            return self.destination.resolver.playlist(self.destination.resolver.get_playlist(id))

        isrcs = []
        match self.source.id:
            case 'deezer':
                for track in self.source.resolver.get_playlist(id):
                    isrcs.append(track['isrc'])
                return self.get_playlist_by_isrc(isrcs)
            case 'spotify':
                for track in self.source.resolver.get_playlist(id):
                    track = track
                    if (track['track'] != True):
                        track = track['track']

                    if ('isrc' not in track['external_ids']):
                        logger.warn(
                            f'Track {track["artists"][0]["name"]} - {track["name"]} does not have an ISRC')
                    else:
                        isrcs.append(track['external_ids']['isrc'])

                return self.get_playlist_by_isrc(isrcs)
            case _:
                raise NotImplementedError('Source type not supported')

    def get_track_by_isrc(self, isrc):
        track = self.destination.resolver.get_track_by_isrc(isrc)
        result = self.destination.resolver.track(track)
        return result

    def get_playlist_by_isrc(self, isrcs):
        playlist = list(self.destination.resolver.get_playlist_by_isrc(isrcs))
        filtered_playlist = list(
            filter(lambda item: item is not None, playlist))
        result = self.destination.resolver.playlist(filtered_playlist)
        return result
