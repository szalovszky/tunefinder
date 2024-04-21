from tunefinder.definitions.Track import Track


class Isrc:
    def __init__(self):
        pass

    def track(self, isrc):
        if isrc is None:
            return None

        return Track(
            platform='isrc',
            id=None,
            title=None,
            artist=None,
            album=None,
            isrc=isrc,
            url=f'isrc://{isrc}')

    def playlist(self, playlist):
        return [self.track(item) for item in playlist]

    def get_track_by_isrc(self, isrc):
        return isrc

    def get_playlist_by_isrc(self, isrcs):
        return isrcs
