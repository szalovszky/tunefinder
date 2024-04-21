from shazamio import Shazam as ShazamIO


class Shazam:
    def __init__(self):
        self.client = ShazamIO(language="EN")

    async def get_track(self, uri):
        id = uri.split('/')[-2]
        track = await self.client.track_about(track_id=id)
        return track
