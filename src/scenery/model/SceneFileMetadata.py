class SceneFileMetadata:
    def __init__(self, show=None, season=None, episode=None, title=None):
        self.show = show
        self.season = season
        self.episode = episode
        self.title = title

    def isComplete(self):
        return (
            self.show is not None and
            self.season is not None and
            self.episode is not None and
            self.title is not None
        )
