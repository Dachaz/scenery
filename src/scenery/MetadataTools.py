import re
import os.path
from scenery.model.SceneFileMetadata import SceneFileMetadata

REGEX_SPLITTER = "([sS]?\\d+?\\s?[eExX-]\\d+)"
REGEX_EPISODE_SPLITTER = "[sS]?(\\d+?)\\s?[eExX-](\\d+)"
REGEX_CLEANER = "[^a-zA-Z0-9]+$"


def extractMetadata(fileName):
    # Normalise to whitespace-separated words
    fileName = re.sub("[._]", " ", fileName)

    # Look for relevant parts
    parts = re.split(REGEX_SPLITTER, fileName)

    # If we can't split into SHOWNAME - SEASON+EPISODE move on.
    if len(parts) < 2:
        return None

    # Additionally clean the show name (remove special characters, capitalise)
    show = re.sub(REGEX_CLEANER, "", parts[0]).title()

    # TODO: Apply substitutions on the show name

    # Get season and episode numbers
    subparts = re.split(REGEX_EPISODE_SPLITTER, parts[1])
    season = int(subparts[1])
    episode = int(subparts[2])

    meta = SceneFileMetadata(show=show, season=season, episode=episode)
    return meta


def generateFilename(sceneFile, pattern, zeroesSeason=False, zeroesEpisodes=False):
    meta = sceneFile.meta
    # Keep the extension of the original file
    extension = os.path.splitext(sceneFile.file)[1]

    # Scenery.app's pattern syntax parsing magic
    episodeString = ('%02d' if zeroesEpisodes else '%d') % meta.episode
    replacements = {
        '%a': str(meta.show),
        '%s': ('%02d' if zeroesSeason else '%d') % meta.season,
        '%n': episodeString,
        '%t': meta.title or 'Episode %s' % episodeString,
    }

    out = pattern
    for symbol, replacement in replacements.items():
        out = out.replace(symbol, replacement)

    return out + extension
