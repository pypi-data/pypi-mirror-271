# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['tracking_markers']

package_data = \
{'': ['*']}

install_requires = \
['numpy>=1.26.1,<2.0.0', 'opencv-python>=4.8.1.78,<5.0.0.0']

entry_points = \
{'console_scripts': ['tracking-markers = '
                     'tracking_markers.tracking_points:main']}

setup_kwargs = {
    'name': 'tracking-markers',
    'version': '0.2.0',
    'description': 'A humble image tracking code',
    'long_description': '# A humble image tracking code\n\n![Made with Python](https://img.shields.io/badge/Made%20with-Python-blue?logo=python&logoColor=ecf0f1&labelColor=34495e)\n[![GitHub license](https://img.shields.io/github/license/bertoldi-collab/tracking-markers?labelColor=34495e)](https://github.com/bertoldi-collab/tracking-markers/blob/main/LICENSE)\n[![Hits](https://hits.seeyoufarm.com/api/count/incr/badge.svg?url=https%3A%2F%2Fgithub.com%2Fbertoldi-collab%2Ftracking-markers&count_bg=%2327AE60&title_bg=%2334495E&icon=github.svg&icon_color=%23E7E7E7&title=Hits&edge_flat=false)](https://hits.seeyoufarm.com)\n\nThis is a humble image tracking code.\nIt is humble because it does what it can.\n\n<p align="center">\n  <img width="460" height="300" src="examples/spaceman.gif">\n</p>\n\n## Installation\n\nAssuming you have access to the repo and ssh keys are set up in your GitHub account, you can install the package with\n\n```bash\npip install git+ssh://git@github.com/bertoldi-collab/tracking-markers.git@main\n```\n\n## How to use\n\n### CLI\n\nRun in a terminal\n\n```bash\ntracking-markers path/to/video.mp4\n```\n\nSee `tracking-markers --help` for more info on all the options.\n\n### Python\n\nThe main module is [`tracking_points.py`](tracking_markers/tracking_points.py) defining the `track_points(...)` function that actually does the tracking of a given video and the function `select_markers(...)` that allows the manual selection of markers.\nThese functions can be used independently.\nThe file [`tracking_points.py`](tracking_markers/tracking_points.py) can also be used as a script.\n\n## Some info\n\n- It is based on the [OpenCV](https://opencv.org/) library.\n- Allows for markers to be manually selected or an `np.ndarray` of markers can be loaded from a file.\n- Works best on high-contrast videos.\n',
    'author': 'Giovanni Bordiga',
    'author_email': 'gbordiga@seas.harvard.edu',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/bertoldi-collab/tracking-markers',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<3.13',
}


setup(**setup_kwargs)
