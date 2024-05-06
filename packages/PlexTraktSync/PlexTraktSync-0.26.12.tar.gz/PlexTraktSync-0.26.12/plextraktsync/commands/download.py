from __future__ import annotations

from os.path import exists
from pathlib import Path, PureWindowsPath
from typing import TYPE_CHECKING

from plextraktsync.factory import factory
from plextraktsync.util.expand_id import expand_id

if TYPE_CHECKING:
    from plextraktsync.plex.PlexApi import PlexApi
    from plextraktsync.plex.PlexLibraryItem import PlexLibraryItem


def download_media(plex: PlexApi, pm: PlexLibraryItem, savepath: Path):
    print(f"Download media for {pm}:")
    for index, part in enumerate(pm.parts, start=1):
        # Remove directory part (Windows server on Unix)
        # plex.download() is able to do that on Unix to Unix server, but not Windows to Unix
        filename = PureWindowsPath(part.file).name
        filename = Path(savepath, filename)

        if exists(filename):
            print(f"Skip existing file: {filename}")
            continue

        print(f"Downloading part {index}: {part.file}")
        print(f"Saving as {filename}")
        plex.download(part, savepath=savepath, filename=filename, showstatus=True)


def download_subtitles(plex: PlexApi, pm: PlexLibraryItem, savepath: Path):
    print(f"Subtitles for {pm}:")
    for index, sub in enumerate(pm.subtitle_streams, start=1):
        print(
            f"  Subtitle {index}: ({sub.language}) {sub.title} (codec: {sub.codec}, selected: {sub.selected}, transient: {sub.transient})"
        )

        filename = ''.join([
            f"{sub.id}. ",
            f"{sub.title}" if sub.title else "",
            f"{sub.language}." if sub.language else "",
            f"{sub.languageCode}.{sub.codec}"
        ])

        filename = Path(savepath, filename)

        if not exists(filename):
            if not sub.key:
                print(f"  ERROR: Subtitle {index}: has no key: Not downloadable")
                continue

            plex.download(sub, savepath=savepath, filename=filename, showstatus=True)
            print(f"Downloaded: {filename}")


def download(input: list[str], only_subs: bool, target: str):
    plex = factory.plex_api
    print = factory.print

    # Expand ~ as HOME
    savepath = Path(target).expanduser()
    for id in expand_id(input):
        pm = plex.fetch_item(id)
        if not pm:
            print(f"Not found: {id}. Skipping")
            continue

        if not only_subs:
            download_media(plex, pm, savepath)

        download_subtitles(plex, pm, savepath)
