import json
import logging
import urllib2
from scenery.model.SceneFileMetadata import SceneFileMetadata
from scenery.model.SceneFileMetadataCache import SceneFileMetadataCache

cache = SceneFileMetadataCache()
TVMAZE_SEARCH_URL = "http://api.tvmaze.com/singlesearch/shows?embed=episodes&q="


def getTitle(meta):
    fetchEpisodes(meta.show)
    return cache.getTitle(meta)


def fetchEpisodes(showName):
    # Make sure to fetch from TVMaze only once per application run
    if cache.hasShow(showName):
        return

    try:
        url = TVMAZE_SEARCH_URL + showName
        response = urllib2.urlopen(url)
        data = json.loads(response.read())

        # If the server decided to return no episode data, mark the show as unknown
        if '_embedded' not in data:
            cache.markAsUnknown(showName)
        else:
            for episode in data['_embedded']['episodes']:
                meta = SceneFileMetadata(
                    show=showName,
                    season=episode['season'],
                    episode=episode['number'],
                    title=episode['name']
                )
                cache.add(meta)

    except BaseException:
        logging.warning("Couldn't find show %s", showName)
        cache.markAsUnknown(showName)
