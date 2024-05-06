<p align="center">
    <img src="https://raw.githubusercontent.com/neufter/downmixer/main/docs/assets/logo_white.svg" style="width: 80vw; max-width: 650px"/>
</p>

Download songs from streaming services easily. Can be an alternative or replacement
to [spotDL](https://github.com/spotDL/spotify-downloader), however, it is **only a Python library, *not* a CLI tool**. A
very simple `download` command is available for convenience only.

It is structured to be platform independent - by default, it syncs Spotify libraries downloaded from either Spotify
itself or YouTube Music, with lyrics from AZLyrics. However, it can be extended to sync from any streaming service using
any audio file source.

## This project is currently in alpha version.

Basic functionality mostly works, with Spotify libraries and YT Music audio sources.

## Usage

### Command line

```shell
downmixer download [spotify id]
```

Downloads the first matched result for a Spotify song ID.

### Use as a library

Downmixer is made to be used as a library by other apps, not by end users. By default, it doesn't provide a large
convenience function
like spotDL's `search()` and `download()` methods.

More info in the documentation: https://neufter.github.io/downmixer/

## Building

```shell
git clone https://github.com/neufter/downmixer
cd downmixer
pipenv install
pip install build
```
