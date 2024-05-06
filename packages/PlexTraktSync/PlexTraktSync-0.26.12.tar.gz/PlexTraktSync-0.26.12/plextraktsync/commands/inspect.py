from __future__ import annotations

from typing import TYPE_CHECKING
from urllib.parse import quote_plus

from plexapi.utils import millisecondToHumanstr

from plextraktsync.factory import factory
from plextraktsync.util.expand_id import expand_id

if TYPE_CHECKING:
    from plextraktsync.media import Media
    from plextraktsync.plex.PlexLibraryItem import PlexLibraryItem


def inspect_media(id: str):
    plex = factory.plex_api
    mf = factory.media_factory
    print = factory.print

    print("")
    pm: PlexLibraryItem = plex.fetch_item(id)
    if not pm:
        print(f"Inspecting {id}: Not found")
        return

    print(f"Inspecting {id}: {pm}")
    if pm.library:
        print(f"Library: {pm.library.title}")

    url = plex.media_url(pm)
    print(f"Plex Web URL: {url}")

    if not pm.is_discover and not pm.is_legacy_agent:
        url = plex.media_url(pm, discover=True)
        print(f"Discover URL: {url}")

    media = pm.item
    print(f"Title: {media.title}")
    if media.type == 'movie' and pm.edition_title:
        print(f"Edition Title: {pm.edition_title}")
    if pm.has_media:
        print(f"Media.Duration: {pm.duration}")
    print(f"Media.Type: '{media.type}'")
    print(f"Media.Guid: '{media.guid}'")
    if not pm.is_legacy_agent:
        print(f"Media.Guids: {media.guids}")

    if not pm.is_discover and media.type in ["episode", "movie"]:
        audio = pm.audio_streams[0]
        print(f"Audio: '{audio.audioChannelLayout}', '{audio.displayTitle}'")

        video = pm.video_streams[0]
        print(f"Video: '{video.codec}'")

        print("Subtitles:")
        for index, subtitle in enumerate(pm.subtitle_streams, start=1):
            print(f"  Subtitle {index}: ({subtitle.language}) {subtitle.title} (codec: {subtitle.codec}, selected: {subtitle.selected}, transient: {subtitle.transient})")

        print("Parts:")
        for index, part in enumerate(pm.parts, start=1):
            print(f"  Part {index}: [link=file://{quote_plus(part.file)}]{part.file}[/link]")

        print("Markers:")
        for marker in pm.markers:
            start = millisecondToHumanstr(marker.start)
            end = millisecondToHumanstr(marker.end)
            print(f"  {marker.type}: {start} - {end}")

    print("Guids:")
    for guid in pm.guids:
        print(f"  Guid: {guid}, Id: {guid.id}, Provider: '{guid.provider}'")

    print(f"Metadata: {pm.to_json()}")

    m: Media = mf.resolve_any(pm)
    if not m:
        print("Trakt: No match found")
        return

    print(f"Trakt: {m.trakt_url}")
    print(f"Plex Rating: {m.plex_rating}")
    print(f"Trakt Rating: {m.trakt_rating}")
    print(f"Watched on Plex: {m.watched_on_plex}")
    if pm.has_media:
        print(f"Watched on Trakt: {m.watched_on_trakt}")
        print(f"Collected on Trakt: {m.is_collected}")

    print("Plex play history:")
    for h in m.plex_history(device=True, account=True):
        d = h.device
        # handle cases like "local" for offline plays
        if d.name == '' and d.platform == '':
            dn = h.device.clientIdentifier
        else:
            dn = f"{d.name} with {d.platform}"
        print(f"- {h.viewedAt} {h}: by {h.account.name} on {dn}")


def inspect(inputs: list[str]):
    print = factory.print
    print(f"PlexTraktSync [{factory.version.full_version}]")

    for id in expand_id(inputs):
        inspect_media(id)
