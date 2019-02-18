import logging
import os
import tempfile
import unittest
from mockito import when, unstub, ANY, ARGS
from shutil import rmtree
from scenery.Options import getOptions
from scenery.Scenery import Scenery


class SceneryTests(unittest.TestCase):
    WORK_DIR = os.path.join(tempfile.gettempdir(), 'scenery-test-files')
    TEST_ROOT = os.path.dirname(__file__)

    def setUp(self):
        # In case an earlier run ended abruptly, clean up
        if os.path.exists(self.WORK_DIR):
            self.tearDown()

        # Generate a bunch of empty scene-release-like files
        os.makedirs(self.WORK_DIR)
        with open(os.path.join(self.TEST_ROOT, 'test-assets', 'releases.txt')) as f:
            for fileName in f:
                open(os.path.join(self.WORK_DIR, fileName.strip()), 'a').close()

        # No logging during tests
        when(logging).warning(ANY, *ARGS).thenReturn(None)
        when(logging).info(ANY, *ARGS).thenReturn(None)

        self.maxDiff = None

    def tearDown(self):
        rmtree(self.WORK_DIR)
        unstub()

    def getTargetFiles(self):
        targetFiles = []
        for root, dirs, files in os.walk(self.WORK_DIR):
            for fileName in sorted(files):
                targetFiles.append(os.path.join(root, fileName))
        return targetFiles

    def generateExpectedFiles(self, expectationsFile):
        expectedFiles = []
        with open(os.path.join(self.TEST_ROOT, 'test-assets', expectationsFile)) as f:
            for fileName in f:
                expectedFiles.append(os.path.join(self.WORK_DIR, fileName.strip()))
        return expectedFiles

    def test_dry_run(self):
        preRunState = self.getTargetFiles()
        opts = getOptions([self.WORK_DIR, '-d'])
        s = Scenery(opts)
        s.run()

        # Confirm that no files have changed during the run
        postRunState = self.getTargetFiles()
        self.assertItemsEqual(preRunState, postRunState)

    def test_defaults(self):
        opts = getOptions([self.WORK_DIR])
        s = Scenery(opts)
        s.run()

        postRunState = self.getTargetFiles()
        self.assertItemsEqual(postRunState, self.generateExpectedFiles('expected-default.txt'))

    def test_overwrite(self):
        opts = getOptions([self.WORK_DIR, '-o'])
        s = Scenery(opts)
        s.run()

        postRunState = self.getTargetFiles()
        self.assertItemsEqual(postRunState, self.generateExpectedFiles('expected-overwrite.txt'))

    def test_force(self):
        opts = getOptions([self.WORK_DIR, '-f'])
        s = Scenery(opts)
        s.run()

        postRunState = self.getTargetFiles()
        self.assertItemsEqual(postRunState, self.generateExpectedFiles('expected-force.txt'))

    def test_episode_zeroes(self):
        opts = getOptions([self.WORK_DIR, '-e'])
        s = Scenery(opts)
        s.run()

        postRunState = self.getTargetFiles()
        self.assertItemsEqual(postRunState, self.generateExpectedFiles('expected-episode-zeroes.txt'))

    def test_season_zeroes(self):
        opts = getOptions([self.WORK_DIR, '-s'])
        s = Scenery(opts)
        s.run()

        postRunState = self.getTargetFiles()
        self.assertItemsEqual(postRunState, self.generateExpectedFiles('expected-season-zeroes.txt'))

    def test_both_zeroes(self):
        opts = getOptions([self.WORK_DIR, '-s', '-e'])
        s = Scenery(opts)
        s.run()

        postRunState = self.getTargetFiles()
        self.assertItemsEqual(postRunState, self.generateExpectedFiles('expected-both-zeroes.txt'))

    def test_pattern_subfolders(self):
        opts = getOptions([self.WORK_DIR, '-p', '%a/Season %s/%s.%n %t', '-e'])
        s = Scenery(opts)
        s.run()

        postRunState = self.getTargetFiles()
        self.assertItemsEqual(postRunState, self.generateExpectedFiles('expected-pattern-subfolders.txt'))

    def test_pattern_subfolders_force(self):
        opts = getOptions([self.WORK_DIR, '-p', '%a/Season %s/%s.%n %t', '-e', '-f'])
        s = Scenery(opts)
        s.run()

        postRunState = self.getTargetFiles()
        self.assertItemsEqual(postRunState, self.generateExpectedFiles('expected-pattern-subfolders-force.txt'))

    def test_single_file(self):
        opts = getOptions([os.path.join(self.WORK_DIR, 'The.Simpsons.01x01.VHS.avi')])
        s = Scenery(opts)
        s.run()

        postRunState = self.getTargetFiles()
        self.assertItemsEqual(postRunState, self.generateExpectedFiles('expected-single-file.txt'))
