import unittest
from scenery.Options import getOptions


# Essentially, the point of this is to capture changes that would break how the script used to be called before
class OptionsTest(unittest.TestCase):
    def test_insufficient_options(self):
        self.assertRaises(BaseException, getOptions, [])

    def test_defaults(self):
        opts = getOptions(['/dl'])
        self.assertEquals(opts.path, '/dl')
        self.assertEquals(opts.pattern, '%a S%sE%n %t')
        self.assertFalse(opts.zeroesSeason)
        self.assertFalse(opts.zeroesEpisodes)
        self.assertFalse(opts.overwrite)
        self.assertFalse(opts.dryRun)
        self.assertFalse(opts.verbose)
        self.assertFalse(opts.force)

    def test_short_syntax(self):
        opts = getOptions(['/dl', '-p', '%s.%n %t', '-s', '-e', '-o', '-d', '-v', '-f'])
        self.assertEquals(opts.path, '/dl')
        self.assertEquals(opts.pattern, '%s.%n %t')
        self.assertTrue(opts.zeroesSeason)
        self.assertTrue(opts.zeroesEpisodes)
        self.assertTrue(opts.overwrite)
        self.assertTrue(opts.dryRun)
        self.assertTrue(opts.verbose)
        self.assertTrue(opts.force)

    def test_long_syntax(self):
        opts = getOptions(['/dl', '--pattern', '%s.%n %t', '--season-zeroes', '--episode-zeroes', '--overwrite', '--dry-run', '--verbose', '--force'])
        self.assertEquals(opts.path, '/dl')
        self.assertEquals(opts.pattern, '%s.%n %t')
        self.assertTrue(opts.zeroesSeason)
        self.assertTrue(opts.zeroesEpisodes)
        self.assertTrue(opts.overwrite)
        self.assertTrue(opts.dryRun)
        self.assertTrue(opts.verbose)
        self.assertTrue(opts.force)
