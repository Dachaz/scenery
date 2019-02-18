import unittest
from scenery.model.SceneFileMetadata import SceneFileMetadata
from scenery.model.SceneFileMetadataCache import SceneFileMetadataCache


class SceneFileMetadataCacheTest(unittest.TestCase):
    def setUp(self):
        self.cache = SceneFileMetadataCache()
        self.cache.clear()
        self.meta1 = SceneFileMetadata(
            show="Bob's Burgers",
            season=9,
            episode=7,
            title='I Bob Your Pardon'
        )
        self.meta2 = SceneFileMetadata(
            show="bobs burgers",
            season=9,
            episode=9,
            title="UFO No You Didn't"
        )

    def test_empty_has_no_shows(self):
        self.assertFalse(self.cache.hasShow("The X-Files"))

    def test_has_no_wrong_show(self):
        self.cache.add(self.meta1)
        self.assertFalse(self.cache.hasShow("The X-Files"))

    def test_has_correct_show_with_different_spellings(self):
        self.cache.add(self.meta1)
        self.assertTrue(self.cache.hasShow("Bob's Burgers"))
        self.assertTrue(self.cache.hasShow("bobs-burgers"))
        self.assertTrue(self.cache.hasShow("BOB'S BURGERS"))

    def test_marking_as_unknown(self):
        self.assertFalse(self.cache.hasShow("The X-Files"))
        self.cache.markAsUnknown("The X-Files")
        self.assertTrue(self.cache.hasShow("The X-Files"))

    def test_getting_existing_titles_from_cache(self):
        # Store two episodes of the same show
        self.cache.add(self.meta1)
        self.cache.add(self.meta2)
        # Verify that we can get both values back
        self.assertEquals(self.cache.getTitle(self.meta1), self.meta1.title)
        self.assertEquals(self.cache.getTitle(self.meta2), self.meta2.title)

    def test_getting_nonexisting_title_from_cache(self):
        # Store one episode in cache
        self.cache.add(self.meta1)
        # Try to get the other one from cache
        self.assertEquals(self.cache.getTitle(self.meta2), None)

    def test_clearing(self):
        self.assertFalse(self.cache.hasShow("Bob's Burgers"))
        self.cache.add(self.meta1)
        self.assertTrue(self.cache.hasShow("Bob's Burgers"))
        self.cache.clear()
        self.assertFalse(self.cache.hasShow("Bob's Burgers"))
