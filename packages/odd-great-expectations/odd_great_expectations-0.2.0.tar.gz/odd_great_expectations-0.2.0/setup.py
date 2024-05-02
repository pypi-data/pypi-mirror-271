# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['odd_great_expectations', 'odd_great_expectations.dataset']

package_data = \
{'': ['*']}

install_requires = \
['funcy>=1.17,<2.0',
 'great-expectations>=0.15.44,<0.16.0',
 'loguru>=0.6.0,<0.7.0',
 'odd-models==2.0.17',
 'oddrn-generator>=0.1.68,<0.2.0',
 'psycopg2>=2.9.5,<3.0.0',
 'sqlalchemy>=1.4.46,<2.0.0']

setup_kwargs = {
    'name': 'odd-great-expectations',
    'version': '0.2.0',
    'description': 'OpenDataDiscovery Action for Great Expectations',
    'long_description': "## OpenDataDiscovery Action for handling Great Expectations tests results.\n\n[![PyPI version](https://badge.fury.io/py/odd-great-expectations.svg)](https://badge.fury.io/py/odd-great-expectations)\n\n![image](assets/screenshot.png)\n\n# What is it?\n`odd_great_expectation.action.ODDAction`\nIs a class derived from GX `ValidationAction` which will be run by GreatExpectations at runtime with `ValidationResult`s for checkpoint.\n\n\n# How to use it?:\nInstall `odd-great-expectations` package\n```bash\npip install odd-great-expectations\n```\nAdd `ODDAction` action to some checkpoint's action list:\n```yaml\nname: <CHECKPOINT_NAME>\nconfig_version: 1.0\n...\naction_list:\n  # other actions\n  - name: store_metadata_to_odd\n    action:\n      module_name: odd_great_expectations.action\n      class_name: ODDAction\n      platform_host: <PLATFORM_HOST>\n      data_source_name: <DATA_SOURCE_NAME>\n```\n\nParameters:\n\n`platform_host` - Location of OpenDataDiscovery platform, i.e. http://localhost:8080\n\n`platform_token` - OpenDataDiscovery token, how to get it - https://docs.opendatadiscovery.org/configuration-and-deployment/trylocally#create-collector-entity\n\n`data_source_name` - Unique name for data source, i.e. local_qa_test\n\nBoth `platform_host` and `platform_token`  can be set using `ODD_PLATFORM_HOST` and `ODD_PLATFORM_PLATFORM` env variables accordingly.\n\nRun checkpoint\n```bash\ngreat_expectations checkpoint run <CHECKPOINT_NAME>\n```\nCheck results on `PLATFORM_HOST` UI.\n\n## Supporting features\n| Feature                     | Supporting |\n| --------------------------- | ---------- |\n| V3 API +                    | +          |\n| SqlAlchemyEngine            | +          |\n| PandasEngine                | +          |\n| Great Expectations V2 API - | -          |\n| Cloud Solution              | -          |\n",
    'author': 'Pavel Makarichev',
    'author_email': 'vixtir90@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
