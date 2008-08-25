#!/usr/bin/env python

import os
import re
from glob import glob

from distutils.core import setup
from distutils.util import change_root, convert_path

from distutils.command.install_data import install_data
from distutils.command.install_scripts import install_scripts
from DistUtilsExtra.command.build_extra import build_extra


def changelog_version(changelog="debian/changelog"):
    version = "dev"
    if os.path.exists(changelog):
        head=open(changelog).readline()
        match = re.compile(".*\((.*)\).*").match(head)
        if match:
            version = match.group(1)

    return version

class testing_install_data(install_data, object):

    def finalize_options(self):
        """Add wildcard support for filenames."""
        super(testing_install_data, self).finalize_options()

        for f in self.data_files:
            if type(f) != str:
                files = f[1]
                i = 0
                while i < len(files):
                    if "*" in files[i]:
                        for e in glob(files[i]):
                            files.append(e)
                        files.pop(i)
                        i -= 1
                    i += 1


setup(
    name = "ubuntu-desktop-testing",
    version = changelog_version(),
    author = "Ara Pulido",
    author_email = "ara.pulido@canonical.com",
    license = "LGPL",
    description = "Ubuntu Desktop Testing",
    long_description = """
This project provides a library and scripts for desktop testing.
""",
    data_files = [
        ("share/ubuntu-desktop-tests/gedit", ["gedit/*.*"]),
        ("share/ubuntu-desktop-tests/gedit/app_data", ["gedit/app_data/*"]),
        ("share/ubuntu-desktop-tests/openAll", ["openAll/*.*"]),
        ("share/ubuntu-desktop-tests/openAll/app_data", ["openAll/app_data/*"]),
        ("share/ubuntu-desktop-tests/updateSystem", ["updateSystem/*"])],
    packages = ["ubuntutesting"],
    cmdclass = {
        "install_data": testing_install_data,
        "build" : build_extra }
)
