#!/usr/bin/env python
#   -*- coding: utf-8 -*-

from setuptools import setup
from setuptools.command.install import install as _install

class install(_install):
    def pre_install_script(self):
        pass

    def post_install_script(self):
        pass

    def run(self):
        self.pre_install_script()

        _install.run(self)

        self.post_install_script()

if __name__ == '__main__':
    setup(
        name = 'pybuilder-git-version',
        version = '0.6.0',
        description = 'A Git versioning plugin for PyBuilder',
        long_description = "PyBuilder Git Version Plugin\n============================\n\nSummary\n-------\n\nThis project is a plugin for [PyBuilder](https://pybuilder.io) that sets the\nproject version based on git tags.\n\nUsage\n-----\n\nTo use the plugin put the following in the plugins section of `build.py`:\n\n```python\nuse_plugin('pybuilder_git_version')\n```\n\nThe possible properties for use are:\n\n| Property                                    | Value        | Default | Usage                                      |\n|---------------------------------------------|--------------|---------|--------------------------------------------|\n| use_git_version                             | True / False | True    | Turns off pybuilder_git_version            |\n| git_version_commit_distance_as_build_number | True / False | True    | Uses commit count from tag as build number |\n\n\nExamples\n--------\n\nThe following table has examples of repo state and corresponding version\nnumber produced.\n\n| Tag        | Branch             | Clean / Dirty | Number of commits since tag | Version                |\n|------------|--------------------|---------------|-----------------------------|------------------------|\n| 0.0.1      | master             | clean         | 0                           | 0.0.1                  |\n| 0.0.1      | master             | dirty         | 0                           | 0.0.2+build.0          |\n| 0.2.2      | develop            | clean         | 5                           | 0.2.3+develop.5        |\n| 1.2.3      | develop            | dirty         | 3                           | 1.2.4+develop.3        |\n| 1.0.0-rc.1 | feature/TICKET-100 | clean         | 5                           | 1.0.0-rc.1+ticket100.5 |\n| 0.0.1      | hotfix/BUG-20      | clean         | 0                           | 0.0.2+bug20.0          |",
        long_description_content_type = 'text/markdown',
        classifiers = [
            'Development Status :: 3 - Alpha',
            'Programming Language :: Python'
        ],
        keywords = '',

        author = 'Jeffrey Sheehan',
        author_email = 'jeff.sheehan7@gmail.com',
        maintainer = '',
        maintainer_email = '',

        license = 'MIT License',

        url = 'https://github.com/jlsheehan/pybuilder-git-version',
        project_urls = {},

        scripts = [],
        packages = ['pybuilder_git_version'],
        namespace_packages = [],
        py_modules = [],
        entry_points = {},
        data_files = [],
        package_data = {},
        install_requires = [
            'gitpython==3.1.43',
            'semver==2.13.0'
        ],
        dependency_links = [],
        zip_safe = True,
        cmdclass = {'install': install},
        python_requires = '',
        obsoletes = [],
    )
