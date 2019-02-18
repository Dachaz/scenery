import unittest
from scenery.model.SceneFileMetadata import SceneFileMetadata


class SceneFileMetadataTest(unittest.TestCase):
    def test_complete_meta(self):
        meta = SceneFileMetadata(
            show='3rd Rock from the Sun',
            season=1,
            episode=15,
            title='I Enjoy Being a Dick'
        )
        self.assertTrue(meta.isComplete())

    def test_incomplete_meta(self):
        meta = SceneFileMetadata(
            show='Dark',
            season=1,
            episode=4
        )
        self.assertFalse(meta.isComplete())
