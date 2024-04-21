class Track:
    def __init__(self, platform: str, id: str | None, title: str | None, artist: str | None, album: str | None, isrc: str, url: str | None = None):
        self.platform = platform
        self.id = id
        self.title = title
        self.artist = artist
        self.album = album
        self.isrc = isrc
        self.url = url
