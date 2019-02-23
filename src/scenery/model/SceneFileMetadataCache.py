import re


class SceneFileMetadataCache:
    # Cache format: dict(show_key => dict(season_number => dict(episode_number => episode_title)))
    __cache = dict()

    # Minimum sanitation to have different spellings point to the same cache
    # (e.g. "bobs burgers" and "Bob's Burgers")
    @classmethod
    def getShowKey(cls, showName):
        return re.sub('[^a-z0-9]', '', showName.lower())

    def hasShow(self, showName):
        return self.getShowKey(showName) in self.__cache

    def add(self, meta):
        key = self.getShowKey(meta.show)

        if key not in self.__cache:
            self.__cache[key] = dict()
        if meta.season not in self.__cache[key]:
            self.__cache[key][meta.season] = dict()
        self.__cache[key][meta.season][meta.episode] = meta.title

    def getTitle(self, meta):
        key = self.getShowKey(meta.show)
        if (
            key in self.__cache and
            meta.season in self.__cache[key] and
            meta.episode in self.__cache[key][meta.season]
        ):
            return self.__cache[key][meta.season][meta.episode]
        return None

    # Store an empty dict to prevent followup requests for this show
    def markAsUnknown(self, showName):
        key = self.getShowKey(showName)
        self.__cache[key] = dict()

    def clear(self):
        self.__cache = dict()
