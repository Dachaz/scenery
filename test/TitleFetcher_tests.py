from mockito import when, mock, unstub, verify, ANY, ARGS
from scenery.TitleFetcher import getTitle, fetchEpisodes, TVMAZE_SEARCH_URL, cache
from scenery.model.SceneFileMetadata import SceneFileMetadata
import logging
import unittest
import urllib2
import os


class TitleFetcherTest(unittest.TestCase):
    def tearDown(self):
        unstub()

    def setUp(self):
        when(logging).warning(ANY, *ARGS).thenReturn(None)
        testRoot = os.path.dirname(__file__)
        # Mock 1: The endpoint returns multiple episodes
        bobData = open(os.path.join(testRoot, 'test-assets', '107.json')).read()
        self.bobResponse = mock()
        when(self.bobResponse).read().thenReturn(bobData)
        bobUrl1 = TVMAZE_SEARCH_URL + 'Bobs Burgers'
        bobUrl2 = TVMAZE_SEARCH_URL + "Bob's Burgers"
        when(urllib2).urlopen(bobUrl1).thenReturn(self.bobResponse)
        when(urllib2).urlopen(bobUrl2).thenReturn(self.bobResponse)

        # Mock 2: The endpoint returns only show info
        xfData = open(os.path.join(testRoot, 'test-assets', '430.json')).read()
        self.xfResponse = mock()
        when(self.xfResponse).read().thenReturn(xfData)
        xfUrl1 = TVMAZE_SEARCH_URL + 'The X-Files'
        xfUrl2 = TVMAZE_SEARCH_URL + 'The X Files'
        when(urllib2).urlopen(xfUrl1).thenReturn(self.xfResponse)
        when(urllib2).urlopen(xfUrl2).thenReturn(self.xfResponse)

    def test_only_one_request_is_sent_to_server_for_shows_with_similar_names(self):
        fetchEpisodes('Bobs Burgers')
        fetchEpisodes("Bob's Burgers")
        verify(self.bobResponse, times=1).read()

    def test_server_doesnt_return_episode_list(self):
        fetchEpisodes('The X-Files')
        fetchEpisodes('The X Files')
        verify(self.xfResponse, times=1).read()

    def test_unknown_show(self):
        showName = 'The Misfits'
        fetchEpisodes(showName)
        # Capture the relevant part of the error message
        verify(logging).warning(ANY, showName)
        # Verify that the show has been marked as known (aka: don't retry getting it)
        self.assertTrue(cache.hasShow(showName))

    def test_titles_can_be_fetched_from_cache(self):
        meta = SceneFileMetadata(
            show="Bob's Burgers",
            season=3,
            episode=12
        )
        self.assertEquals(getTitle(meta), 'Broadcast Wagstaff School News')
