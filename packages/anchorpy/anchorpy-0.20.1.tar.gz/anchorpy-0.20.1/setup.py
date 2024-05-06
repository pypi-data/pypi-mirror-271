# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['anchorpy',
 'anchorpy.clientgen',
 'anchorpy.coder',
 'anchorpy.program',
 'anchorpy.program.namespace',
 'anchorpy.utils']

package_data = \
{'': ['*']}

install_requires = \
['anchorpy-core>=0.2.0,<0.3.0',
 'based58>=0.1.1,<0.2.0',
 'borsh-construct>=0.1.0,<0.2.0',
 'construct-typing>=0.5.1,<0.6.0',
 'more-itertools>=8.11.0,<9.0.0',
 'pyheck>=0.1.4,<0.2.0',
 'solana>=0.33.0,<1.0',
 'solders>=0.21.0,<0.22.0',
 'toml>=0.10.2,<0.11.0',
 'toolz>=0.11.2,<0.12.0',
 'websockets>=9.0,<11.0']

extras_require = \
{'cli': ['typer==0.4.1',
         'ipython>=8.0.1,<9.0.0',
         'genpy>=2021.1,<2022.0',
         'black>=22.3.0,<23.0.0',
         'autoflake>=1.4,<2.0'],
 'pytest': ['pytest>=7.2.0,<8.0.0',
            'pytest-xprocess>=0.18.1,<0.19.0',
            'pytest-asyncio>=0.21.0,<0.22.0',
            'py>=1.11.0,<2.0.0']}

entry_points = \
{'console_scripts': ['anchorpy = anchorpy.cli:app'],
 'pytest11': ['pytest_anchorpy = anchorpy.pytest_plugin']}

setup_kwargs = {
    'name': 'anchorpy',
    'version': '0.20.1',
    'description': 'The Python Anchor client.',
    'long_description': '# AnchorPy\n<div align="center">\n    <img src="https://raw.githubusercontent.com/kevinheavey/anchorpy/main/docs/img/logo.png" width="40%" height="40%">\n</div>\n\n---\n\n[![Discord Chat](https://img.shields.io/discord/889577356681945098?color=blueviolet)](https://discord.gg/sxy4zxBckh)  \n\nAnchorPy is the gateway to interacting with [Anchor](https://github.com/project-serum/anchor) programs in Python.\nIt provides:\n\n- A static client generator\n- A dynamic client similar to `anchor-ts`\n- A Pytest plugin\n- A CLI with various utilities for Anchor Python development.\n\nRead the [Documentation](https://kevinheavey.github.io/anchorpy/).\n\n\n\n## Installation (requires Python >=3.9)\n\n```sh\npip install anchorpy[cli, pytest]\n\n```\nOr, if you\'re not using the CLI or Pytest plugin features of AnchorPy you can just run `pip install anchorpy`.\n\n### Development Setup\n\nIf you want to contribute to AnchorPy, follow these steps to get set up:\n\n1. Install [poetry](https://python-poetry.org/docs/#installation)\n2. Install dev dependencies:\n```sh\npoetry install\n\n```\n3. Activate the poetry shell:\n```sh\npoetry shell\n\n```\n',
    'author': 'kevinheavey',
    'author_email': 'kevinheavey123@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/kevinheavey/anchorpy',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
