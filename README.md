<span style="display:block;text-align:center">![Scenery.app icon](https://apps.dachaz.net/IMG/scenery/Scenery.png)</span>

# Scenery

A command-line tool that automates renaming of so-called "Scene Release" files by fetching episode names (from TVMaze) and which uses pattern-based generic building blocks (show name, season number, episode number, episode title) to format the output.

Essentially, a Python-based port of [Scenery.app](http://apps.dachaz.net/scenery/) which was originally available exclusively for macOS.

The intended goal of this port is to be compatible with more platforms, including NASes. (e.g. **WD My Cloud Mirror Gen 2**).

# Installation

## Using pip (cross-platform)

Almost all systems running Python have [pip](https://pip.pypa.io/). On those systems, installation is as easy as:

```bash
pip install scenery
```

## On WD My Cloud Mirror Gen 2

1. Download a precompiled binary from the releases page (e.g. `WDMyCloudMirrorGen2_scenery_1.0.0.bin(18022019)`)
1. Log into the _WD My Cloud Mirror_ admin interface of your device
1. Click "Apps"
1. Click "Install an app manually"
1. Choose the binary you downloaded previously
1. Wait for the confirmation

⚠️ This will only install the command-line utility. You'll still have to ssh into the device to use it!

# Usage
```
usage: scenery [-h] [-p PATTERN] [-s] [-e] [-o] [-d] [-v] [-f] path

positional arguments:
  path                  Which path to process.
                        If a directory is given, it's scanned recursively and all files are processed.
                        If a file is given, only it is processed.

optional arguments:
  -p PATTERN, --pattern PATTERN
                        Output format pattern. Syntax:
                            %a - Show name,
                            %s - Season #,
                            %n - Season #,
                            %t - Episode title
                        (default: "%a S%sE%n %t")
  -s, --season-zeroes   Leading zeroes in season numbers
  -e, --episode-zeroes  Leading zeroes in episode numbers
  -o, --overwrite       Overwrite existing target files
  -d, --dry-run         Do not do the actual renaming, but just show what
                        would happen instead
  -v, --verbose         Output successful actions as well
  -f, --force           Rename files even if the show name couldn't be
                        resolved
```

# Developer notes

The project has been implemented in Python 2 to be compatible with a fairly outdated NAS that is running it.

For the main part of the codebase, [PyBuilder](http://pybuilder.github.io) is used to do analysis (flake8, coverage), run the tests tests and bundle the package.

```bash
$ git clone https://github.com/dachaz/scenery
$ cd scenery
$ pyb
```

The NAS-specific part of the codebase is in the `wdc` folder.

To compile a binary that My Cloud OS3-based NAS will want to install, it needs to be packaged with `mksapkg`. Since this is a proprietary WD binary, I'm not allowed to include it in the codebase. Furthermore, `mksapkg` has a bunch of platform-specific dependencies that my machine didn't meet, so I bundled all of them in a Docker image, including a step that downloads `mksapkg` from WDC. Thus, to build a binary of `scenery` that will run on your NAS, you just need to have Docker running and run:

```bash
$ ./wdc/build.sh
```

To understand the full building process of a My Cloud OS3 binary, please refer to [My Cloud OS3 SDK](https://developer.westerndigital.com/develop/wd/sdk.html).

# License

Copyright © 2019 Dachaz. This software is licensed under the **MIT License**.
