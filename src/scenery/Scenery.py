import logging
import os
from scenery.model.SceneFile import SceneFile
from scenery.MetadataTools import extractMetadata, generateFilename
from scenery.TitleFetcher import getTitle


class Scenery():
    def __init__(self, options):
        self.options = options

    def run(self):
        sceneFiles = self.__listFiles(self.options.path)
        for sceneFile in sceneFiles:
            # Extract basic metadata from the filename
            meta = extractMetadata(sceneFile.file)
            if meta is None:
                logging.warning("Couldn't parse %s", sceneFile.file)
                continue
            sceneFile.meta = meta
            # Fetch the episode title from TVMaze
            sceneFile.meta.title = getTitle(sceneFile.meta)
            # Do the actual renaming
            self.__renameFile(sceneFile)

    @classmethod
    def __listFiles(cls, path):
        sceneFiles = []
        if os.path.isfile(path):
            (root, fileName) = os.path.split(path)
            sceneFile = SceneFile(fileName, root)
            sceneFiles.append(sceneFile)
        else:
            for root, _, files in os.walk(path):
                for fileName in sorted(files):
                    sceneFile = SceneFile(fileName, root)
                    sceneFiles.append(sceneFile)

        return sceneFiles

    def __renameFile(self, sceneFile):
        if not sceneFile.meta.isComplete() and not self.options.force:
            logging.warning("No title found for %s, skipping", sceneFile.file)
            return

        # Generate the target filename and the full path
        targetFile = generateFilename(
            sceneFile=sceneFile,
            pattern=self.options.pattern,
            zeroesSeason=self.options.zeroesSeason,
            zeroesEpisodes=self.options.zeroesEpisodes)
        targetPath = os.path.join(sceneFile.root, targetFile)
        targetDir = os.path.dirname(targetPath)
        sourcePath = os.path.join(sceneFile.root, sceneFile.file)

        # Unless we're happy overwriting, make sure that the target file name is unique
        if os.path.exists(targetPath) and not self.options.overwrite:
            targetParts = os.path.splitext(targetPath)
            i = 1
            while os.path.exists(targetPath):
                targetPath = "%s (%d)%s" % (targetParts[0], i, targetParts[1])
                i += 1

        if self.options.dryRun or self.options.verbose:
            logging.getLogger().setLevel(logging.INFO)
            logging.info("Renaming: %s to %s", sourcePath, targetPath)

        if self.options.dryRun:
            return

        # Create all necessary sub folders
        if not os.path.exists(targetDir):
            os.makedirs(targetDir)
        # Rename
        os.rename(sourcePath, targetPath)
