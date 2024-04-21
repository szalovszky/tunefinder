# tunefinder

Tunefinder is a Python program designed to help you find a song from a source streaming platform on a target streaming platform. With Tunefinder, you can say goodbye to the hassle of manually finding thousands of your favorite tracks on different platforms.

## Supported platforms

- Spotify - source and destination
- Deezer - source and destination
- Shazam - source only
- ISRC - source and destination

## Requirements

- Python 3.10 or higher

## Installation

Clone the repository and install the program:

```bash
git clone https://github.com/szalovszky/tunefinder.git
cd tunefinder
pip install .
```

Now you can use the `tunefinder` command anywhere.

## Usage

```bash
tunefinder [-h] [--minimal] [--output-format] source_uri destination_name
```

### Arguments

- `source_uri`: The URL of the song on the source streaming platform.
- `destination_name`: The target platform where you want to find the song. (Choices: spotify, deezer)

### Options

- `--minimal`, `-m`: Generate minimal output (default: False).
- `--output-format {json,txt}`, `-f {json,txt}`: Specify the output format, either JSON or plain text (default: JSON).

### Credentials

For certain APIs, you'll need to provide API credentials as environment variables.

- #### Spotify

Instructions for obtaining a Client ID and a Client secret can be found [here](https://developer.spotify.com/documentation/web-api/tutorials/getting-started#request-an-access-token).

Then, set the Client ID and Client secret as environment variables:

```bash
export SPOTIFY_CLIENT_ID="46586dec22c390d789a48eb94e0e8060"
export SPOTIFY_CLIENT_SECRET="b636e9720c1e48b60c31482e30a4fba3"
```

- #### Deezer

*This platform doesn't require API credentials*

- #### Shazam

*This platform doesn't require API credentials*

### Examples

This command will find the songs from a playlist **from Spotify on Deezer** and export the result in a **JSON file**:

```bash
tunefinder https://open.spotify.com/playlist/37i9dQZF1DX1qNZsqIInBz deezer
```

This command will find the songs from a playlist **from Spotify on Deezer** and export the result in a **JSON file** without including information about the source and destination:

```bash
tunefinder -m https://open.spotify.com/playlist/37i9dQZF1DX1qNZsqIInBz deezer
```

This command will find the songs from a playlist **from Deezer on Spotify** and export the links in a **TXT file**:

```bash
tunefinder -f txt https://www.deezer.com/us/playlist/10641728502 spotify
```

## License

tunefinder is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Support and Contributions

For bug reports, feature requests, or contributions, please open an issue or submit a pull request on the [GitHub repository](https://github.com/szalovszky/tunefinder).
