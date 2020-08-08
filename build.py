from pybuilder.core import init, use_plugin, Author

use_plugin('python.core')
use_plugin('python.flake8')
use_plugin('python.unittest')
use_plugin('python.coverage')
use_plugin('python.distutils')
use_plugin("python.install_dependencies")

authors = [Author('Dachaz', 'dachaz@dachaz.net')]
license = 'MIT'
name = 'scenery'
summary = 'A pattern-based scene release renamer'
description = """A command-line tool that automates renaming of so-called "Scene Release"
files by fetching episode names (from TVMaze) and which uses pattern-based generic building
blocks (show name, season number, episode number, episode title) to format the output.
"""
url = 'https://github.com/dachaz/scenery'
version = '1.0.1'
requires_python = ">=2.7"

default_task = ["install_dependencies", "analyze", "publish"]


@init
def initialize(project):
    project.build_depends_on('mockito')

    project.set_property('dir_source_main_python', 'src')
    project.set_property('dir_source_unittest_python', 'test')

    project.set_property('flake8_break_build', True)
    project.set_property('flake8_include_test_sources', True)
    project.set_property('flake8_include_scripts', True)

    # relevant tests are in Scenery_tests.py
    project.get_property('coverage_exceptions').append('scenery.__main__')
    project.get_property('coverage_exceptions').append('scenery')

    project.set_property('distutils_console_scripts', ['scenery = scenery:main'])
    project.set_property('distutils_classifiers', [
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Development Status :: 5 - Production/Stable',
        'Environment :: Console',
        'Intended Audience :: End Users/Desktop',
        'License :: OSI Approved :: MIT License',
        'Topic :: Communications :: File Sharing',
        'Topic :: Multimedia',
        'Topic :: Multimedia :: Video',
        'Topic :: Utilities'
    ])
