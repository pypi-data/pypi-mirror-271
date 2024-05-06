# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['satsync', 'satsync.lightglue']

package_data = \
{'': ['*']}

install_requires = \
['kornia>=0.7.2',
 'numpy>=1.25.2',
 'opencv-python>=4.8.0.76',
 'pandas>=2.0.3',
 'rasterio>=1.3.10',
 'scikit-image>=0.19.3',
 'torch>=2.2.0',
 'xarray>=2023.7.0']

setup_kwargs = {
    'name': 'satsync',
    'version': '0.0.4',
    'description': 'A python package to align satellite images.',
    'long_description': '# satsync\n\n[![Release](https://img.shields.io/github/v/release/csaybar/satsync)](https://img.shields.io/github/v/release/csaybar/satsync)\n[![Build status](https://img.shields.io/github/actions/workflow/status/csaybar/satsync/main.yml?branch=main)](https://github.com/csaybar/satsync/actions/workflows/main.yml?query=branch%3Amain)\n[![codecov](https://codecov.io/gh/csaybar/satsync/branch/main/graph/badge.svg)](https://codecov.io/gh/csaybar/satsync)\n[![Commit activity](https://img.shields.io/github/commit-activity/m/csaybar/satsync)](https://img.shields.io/github/commit-activity/m/csaybar/satsync)\n[![License](https://img.shields.io/github/license/csaybar/satsync)](https://img.shields.io/github/license/csaybar/satsync)\n\nA python package to align satellite images.\n\n- **Github repository**: <https://github.com/csaybar/satsync/>\n- **Documentation** <https://csaybar.github.io/satsync/>\n\n## Getting started with your project\n\nFirst, create a repository on GitHub with the same name as this project, and then run the following commands:\n\n```bash\ngit init -b main\ngit add .\ngit commit -m "init commit"\ngit remote add origin git@github.com:csaybar/satsync.git\ngit push -u origin main\n```\n\nFinally, install the environment and the pre-commit hooks with\n\n```bash\nmake install\n```\n\nYou are now ready to start development on your project!\nThe CI/CD pipeline will be triggered when you open a pull request, merge to main, or when you create a new release.\n\nTo finalize the set-up for publishing to PyPi or Artifactory, see [here](https://fpgmaas.github.io/cookiecutter-poetry/features/publishing/#set-up-for-pypi).\nFor activating the automatic documentation with MkDocs, see [here](https://fpgmaas.github.io/cookiecutter-poetry/features/mkdocs/#enabling-the-documentation-on-github).\nTo enable the code coverage reports, see [here](https://fpgmaas.github.io/cookiecutter-poetry/features/codecov/).\n\n## Releasing a new version\n\n- Create an API Token on [Pypi](https://pypi.org/).\n- Add the API Token to your projects secrets with the name `PYPI_TOKEN` by visiting [this page](https://github.com/csaybar/satsync/settings/secrets/actions/new).\n- Create a [new release](https://github.com/csaybar/satsync/releases/new) on Github.\n- Create a new tag in the form `*.*.*`.\n\nFor more details, see [here](https://fpgmaas.github.io/cookiecutter-poetry/features/cicd/#how-to-trigger-a-release).\n\n---\n\nRepository initiated with [fpgmaas/cookiecutter-poetry](https://github.com/fpgmaas/cookiecutter-poetry).\n',
    'author': 'Cesar Aybar',
    'author_email': 'fcesar.aybar@uv.es',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/csaybar/satsync',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
