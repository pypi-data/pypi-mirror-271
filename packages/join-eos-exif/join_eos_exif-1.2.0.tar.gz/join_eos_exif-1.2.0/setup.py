# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['join_eos_exif']

package_data = \
{'': ['*']}

install_requires = \
['PyQt6>=6.4.0,<7.0.0', 'numpy>=1.23.5,<2.0.0', 'pandas>=2.0.1,<3.0.0']

setup_kwargs = {
    'name': 'join-eos-exif',
    'version': '1.2.0',
    'description': 'Join EOS files to images using EXIF data',
    'long_description': '# EOS-EXIF-Join\n\nApplication to join EOS and EXIF data files for image processing\n\nUI made with PyQt6\nexe generated using Pyinstaller\n\n## Installation\n\nInstall the poetry package manager then:\n\n```sh\npoetry install\n```\n\n## Running\n\nUse join_data.exe or\n\n```sh\npoetry run python -m gui\n```\n\n## Building\n\nBuilds are done automatically with GitHub Actions when pushing a tag with a semantic\nversion formats like `vN.N.N` or `vN.N.N-rcN`\n',
    'author': 'Taylor Denouden',
    'author_email': 'taylor.denouden@hakai.org',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8.1,<3.11',
}


setup(**setup_kwargs)
