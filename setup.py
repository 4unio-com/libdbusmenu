#!/usr/bin/env python

import os
import re
from glob import glob
from tempfile import mkstemp

from distutils.core import setup

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

def substitute_variables(infile, outfile, variables={}):
    descriptor_in = open(infile, "r")
    descriptor_out = open(outfile, "w")
    for line in descriptor_in.readlines():
        for key, value in variables.items():
            line = line.replace(key, value)
        descriptor_out.write(line)

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

    def run(self):
        """Run substitutions on files."""
        super(testing_install_data, self).run()

        xmlfiles = [o for o in self.outfiles if o.endswith(".xml")]
        if not xmlfiles:
            return

        # Determine absolute path to share directory
        xslfile = [o for o in self.outfiles
            if os.path.basename(o) == "report.xsl"][0]
        sharedir = os.path.dirname(xslfile)
        if self.root:
            sharedir = sharedir.replace(self.root, os.sep)

        for xmlfile in xmlfiles:
            tmpfile = mkstemp()[1]
            substitute_variables(xmlfile, tmpfile, {
                ">.": ">%s" % sharedir})
            os.rename(tmpfile, xmlfile)

class testing_install_scripts(install_scripts, object):

    def run(self):
        """Run substitutions on files."""
        super(testing_install_scripts, self).run()

        # Substitute directory in defaults.py
        for outfile in self.outfiles:
            infile = os.path.join("bin", os.path.basename(outfile))
            substitute_variables(infile, outfile, {
                'TESTS_SHARE = "."':
                'TESTS_SHARE = "/usr/share/ubuntu-desktop-tests"'})


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
        ("share/ubuntu-desktop-tests", ["report.xsl", "conffile.ini"]),
        ("share/ubuntu-desktop-tests/gedit", ["gedit/*.*"]),
        ("share/ubuntu-desktop-tests/gedit/data", ["gedit/data/*"]),
        ("share/ubuntu-desktop-tests/gnome-panel", ["gnome-panel/*.*"]),
        ("share/ubuntu-desktop-tests/gnome-panel/data", ["gnome-panel/data/*"]),
        ("share/ubuntu-desktop-tests/update-manager", ["update-manager/*.*"]),
        ("share/ubuntu-desktop-tests/update-manager/data", ["update-manager/data/*"]),
        ("share/ubuntu-desktop-tests/seahorse", ["seahorse/*.*"]),
        ("share/ubuntu-desktop-tests/seahorse/data", ["seahorse/data/*"])],
    scripts = ["bin/ubuntu-desktop-test"],
    packages = ["desktoptesting"],
    cmdclass = {
        "install_data": testing_install_data,
        "install_scripts": testing_install_scripts,
        "build" : build_extra }
)
