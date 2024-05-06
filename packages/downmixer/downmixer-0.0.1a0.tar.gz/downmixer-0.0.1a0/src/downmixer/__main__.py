import argparse
import asyncio
import logging
import os
import tempfile
from pathlib import Path

from downmixer import processing, log
from downmixer import providers
from downmixer.providers import ResourceType

logger = logging.getLogger("downmixer").getChild(__name__)

parser = argparse.ArgumentParser(
    prog="downmixer", description="Easily sync tracks from Spotify."
)
parser.add_argument("procedure", choices=["download"])
parser.add_argument(
    "id",
    help="A valid Spotify ID, URI or URL for a track, album or playlist.",
)
parser.add_argument(
    "-o",
    "--output-folder",
    type=Path,
    default=os.curdir,
    dest="output",
    help="Path to the folder in which the final processed files will be placed.",
)
parser.add_argument(
    "-ip",
    "--info-provider",
    type=str,
    default="SpotifyInfoProvider",
    choices=[x.__name__ for x in providers.get_all_info_providers()],
    help=f"Info provider extending BaseInfoProvider to use. Defaults to 'SpotifyInfoProvider'.",
)
parser.add_argument(
    "-ap",
    "--audio-provider",
    type=str,
    default="YouTubeMusicAudioProvider",
    choices=[x.__name__ for x in providers.get_all_audio_providers()],
    help=f"Audio provider extending BaseAudioProvider to use. Defaults to 'YouTubeMusicAudioProvider'.",
)
parser.add_argument(
    "-lp",
    "--lyrics-provider",
    type=str,
    default="AZLyricsProvider",
    choices=[x.__name__ for x in providers.get_all_lyrics_providers()],
    help=f"Lyrics provider extending BaseLyricsProvider to use. Defaults to 'AZLyricsProvider'.",
)
args = parser.parse_args()


def command_line():
    log.setup_logging(debug=True)

    if args.procedure == "download":
        logger.debug("Running download command")

        with tempfile.TemporaryDirectory() as temp:
            logger.debug(f"temp folder: {temp}")

            processor = processing.BasicProcessor(
                [
                    x
                    for x in providers.get_all_info_providers()
                    if x.__name__ == args.info_provider
                ][0](),
                [
                    x
                    for x in providers.get_all_audio_providers()
                    if x.__name__ == args.audio_provider
                ][0](),
                [
                    x
                    for x in providers.get_all_lyrics_providers()
                    if x.__name__ == args.lyrics_provider
                ][0](),
                args.output,
                Path(temp),
            )

            logger.debug(
                f"Initialized processor with providers: {processor.info_provider.__class__.__name__}, "
                f"{processor.audio_provider.__class__.__name__}, "
                f"{processor.lyrics_provider.__class__.__name__}"
            )

            if not processor.info_provider.check_valid_url(
                args.id,
                [ResourceType.SONG, ResourceType.PLAYLIST, ResourceType.ALBUM],
            ):
                raise ValueError("id provided isn't valid")
            rtype = processor.info_provider.get_resource_type(args.id)

            if rtype == ResourceType.SONG:
                logger.debug("Downloading one track")
                asyncio.run(processor.process_song(args.id))
            else:
                logger.debug("Downloading many tracks")
                loop = asyncio.new_event_loop()
                loop.run_until_complete(processor.process_playlist(args.id))
                loop.close()

    exit()


command_line()
