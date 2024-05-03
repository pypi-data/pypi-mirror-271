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
    'version': '0.0.6',
    'description': 'A package for Amazon SDK',
    'long_description': '# Amazon SDK\n\n## Setup\n\n1. Install the package:\n\n```bash\npip install --upgrade Amazon_SDK\n```\n\n2. Add file `.env` with the following content:\n\n```plaintext\nLWA_APP_ID=<your_app_id>\nLWA_CLIENT_SECRET=<your_client_secret>\nSP_API_REFRESH_TOKEN=<your_refresh_token>\n```\n\n## Usage\n\nFor example see `usage_example.py`\n\nDifferences with `bol_SDK`:\n- Use methods in class `AmazonSDK`, with detailed documentation\n- No need to pass `access_token` as a parameter, which is automatically handled by the SDK\n\n',
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
