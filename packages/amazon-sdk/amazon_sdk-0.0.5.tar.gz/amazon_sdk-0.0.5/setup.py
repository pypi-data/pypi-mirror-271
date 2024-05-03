# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['Amazon_SDK']

package_data = \
{'': ['*']}

install_requires = \
['python-dotenv>=1.0.1,<2.0.0', 'requests>=2.31.0,<3.0.0']

setup_kwargs = {
    'name': 'amazon-sdk',
    'version': '0.0.5',
    'description': 'A package for Amazon SDK',
    'long_description': '# Amazon SDK\n\n## Installation\n\n```bash\npip install --upgrade --index-url https://test.pypi.org/simple/ --no-deps Amazon-SDK \n```\n\n## Usage\n\nDifferences with bol_sdk:\n- Use methods in class `AmazonSDK`, with detailed documentation\n- No need to pass the `access_token`\n\nFor example see `usage_example.py`',
    'author': 'Genhao Li',
    'author_email': 'ligenhao20010916@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
