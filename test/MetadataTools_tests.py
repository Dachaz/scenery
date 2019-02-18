import unittest
from scenery.MetadataTools import extractMetadata, generateFilename
from scenery.model.SceneFile import SceneFile
from scenery.model.SceneFileMetadata import SceneFileMetadata


class MetadataToolsTest(unittest.TestCase):
    def setUp(self):
        self.testFile = SceneFile('test.mkv', '/dl')
        self.testFile.meta = SceneFileMetadata(
            show='Black Mirror',
            season=1,
            episode=3,
            title='The Entire History of You'
        )
        self.pattern = '%a/Season %s/%s.%n - %t'

    def test_extract_metadata_from_s01e02_format(self):
        meta = extractMetadata('Star.Trek.Discovery.S02E03.Point.of.Light.1080p.AMZN.WEB-DL.AAC5.1.x265-DDLTV.mkv')
        self.assertEqual(meta.show, 'Star Trek Discovery')
        self.assertEqual(meta.season, 2)
        self.assertEqual(meta.episode, 3)

    def test_extract_metadata_from_01x02_format(self):
        meta = extractMetadata('QI.16x10.720p.iP.WEB-DL.AAC2.0.h264-BTW.mp4')
        self.assertEqual(meta.show, 'Qi')
        self.assertEqual(meta.season, 16)
        self.assertEqual(meta.episode, 10)

    def test_unknown_format(self):
        meta = extractMetadata('Helloween - Keeper of the Seven Keys.mp3')
        self.assertEqual(meta, None)

    def test_generate_filename_pattern_only(self):
        targetFilename = generateFilename(self.testFile, self.pattern)
        self.assertEqual(targetFilename, 'Black Mirror/Season 1/1.3 - The Entire History of You.mkv')

    def test_generate_filename_zeroes_season(self):
        targetFilename = generateFilename(self.testFile, self.pattern, zeroesSeason=True)
        self.assertEqual(targetFilename, 'Black Mirror/Season 01/01.3 - The Entire History of You.mkv')

    def test_generate_filename_zeroes_episodes(self):
        targetFilename = generateFilename(self.testFile, self.pattern, zeroesEpisodes=True)
        self.assertEqual(targetFilename, 'Black Mirror/Season 1/1.03 - The Entire History of You.mkv')

    def test_generate_filename_zeroes_both(self):
        targetFilename = generateFilename(self.testFile, self.pattern, zeroesSeason=True, zeroesEpisodes=True)
        self.assertEqual(targetFilename, 'Black Mirror/Season 01/01.03 - The Entire History of You.mkv')

    def test_generate_filename_unknown_episode_title(self):
        testFile = SceneFile('test2.avi', '/dl')
        testFile.meta = SceneFileMetadata(
            show='Cold Feet',
            season=2,
            episode=4
        )
        targetFilename = generateFilename(testFile, self.pattern)
        self.assertEqual(targetFilename, 'Cold Feet/Season 2/2.4 - Episode 4.avi')
