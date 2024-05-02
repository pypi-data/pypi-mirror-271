# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['aws_ssm_juggle']

package_data = \
{'': ['*']}

install_requires = \
['boto3', 'configargparse', 'shtab', 'simple_term_menu']

entry_points = \
{'console_scripts': ['ec2-juggle = aws_ssm_juggle.ec2:run',
                     'ecs-juggle = aws_ssm_juggle.ecs:run']}

setup_kwargs = {
    'name': 'aws-ssm-juggle',
    'version': '24.5.0',
    'description': 'AWS SSM tool for ECS/EC2 (Shell, Port Forwarding, ...)',
    'long_description': '# aws-ssm-juggle\n\n## Installation\n\n```\npip install aws-ssm-juggle\n```\n\n## Pre-requisites\n\n### [session-manager-plugin](https://docs.aws.amazon.com/systems-manager/latest/userguide/session-manager-working-with-install-plugin.html)\n\n#### Linux\n\n```bash\ncurl https://s3.amazonaws.com/session-manager-downloads/plugin/latest/ubuntu_64bit/session-manager-plugin.deb -o "/tmp/session-manager-plugin.deb"\nmkdir -p ~/bin\ndpkg-deb --fsys-tarfile /tmp/session-manager-plugin.deb | tar --strip-components=4 -C ~/bin/ -xvf - usr/local/sessionmanagerplugin/bin/session-manager-plugin\n```\n\n#### MacOS\n\n`brew install --cask session-manager-plugin`\n\n### Infrastructure\n\nUse [ecs-exec-checker](https://github.com/aws-containers/amazon-ecs-exec-checker) to check for the pre-requisites to use ECS exec.\n\n## ecs-juggle\n\nInspired by [ecsgo](https://github.com/tedsmitt/ecsgo).\n\nProvides a tool to interact with AWS ECS tasks.\n\nCurrently provides:\n\n* interactive execute-command (e.g. shell)\n* port-forwarding\n\nYou can supply command-line arguments to specify which cluster/service/task/... to use or will be prompted with a nice menu.\n\n\n### Usage\n\nSee `ecs-juggle --help` for all features.\n\n#### Execute command\n\nSelect all from menu:\n\n```bash\necs-juggle command\n```\n\n#### Port forwarding\n\nSelect all from menu:\n\n```bash\necs-juggle forward\n```\n\nSpecify port and select the rest from menu:\n\n```bash\necs-juggle forward --remote-port 8080\n```\n\n## ec2-juggle\n\nInspired by [gossm](https://github.com/gjbae1212/gossm/).\n\nProvides a tool to interact with AWS EC2 instances.\n\nCurrently provides:\n\n* interactive shell (e.g. shell)\n* ssh shell\n* port-forwarding\n\n### Usage\n\nSee `ec2-juggle --help` for all features.\n\n#### Start session\n\n```bash\nec2-juggle start\n```\n\n#### Start ssh session\n\nDefault:\n\n```bash\nec2-juggle ssh\n```\n\nWith extra arguments:\n\n```bash\nec2-juggle ssh --ssh-args="-o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null -l ubuntu"\n```\n\n#### Port forwarding\n\n```bash\necs-juggle forward --remote-port 80\n```\n',
    'author': 'Stefan Heitmüller',
    'author_email': 'stefan.heitmueller@gmx.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/morph027/aws-ssm-juggle',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
}


setup(**setup_kwargs)
