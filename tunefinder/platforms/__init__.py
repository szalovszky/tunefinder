from urllib.parse import urlparse

SUPPORTED_DESTINATION_PLATFORMS = ['deezer', 'spotify', 'isrc']


def get(platform: str):
    match platform:
        case 'isrc':
            from .isrc import Isrc
            return Isrc()
        case 'deezer':
            from .deezer import Deezer
            return Deezer()
        case 'spotify':
            from .spotify import Spotify
            return Spotify()
        case 'shazam':
            from .shazam import Shazam
            return Shazam()
        case _:
            raise ValueError(f'Unsupported platform: {platform}')


def get_id_by_url(url: str):
    parsed_url = urlparse(url)
    match parsed_url.netloc:
        case 'deezer.com' | 'www.deezer.com':
            return 'deezer'
        case 'open.spotify.com':
            return 'spotify'
        case 'www.shazam.com' | 'shazam.com':
            return 'shazam'
        case _:
            match parsed_url.scheme:
                case 'spotify' | 'isrc':
                    return parsed_url.scheme
                case _:
                    raise ValueError(f'Unsupported platform: {url}')
