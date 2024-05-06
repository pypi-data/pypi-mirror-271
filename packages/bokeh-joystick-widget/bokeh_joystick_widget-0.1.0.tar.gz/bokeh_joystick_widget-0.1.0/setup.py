# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['bokeh_joystick_widget']

package_data = \
{'': ['*']}

install_requires = \
['bokeh>=3.4.1,<4.0.0']

setup_kwargs = {
    'name': 'bokeh-joystick-widget',
    'version': '0.1.0',
    'description': 'A Bokeh on screen gesture/mouse drag based joystick widget for use in a dashboard with controls',
    'long_description': '# Bokeh Joystick Widget\n\nThis is a custom widget for the Python Bokeh library that allows you to control a joystick via mouse drags or touch gestures.\n\nThe widget has x and y properties that are updated as the joystick is moved. The x and y properties are in the range -100 to 100.\n\nThe widget makes use of <https://github.com/bobboteck/JoyStick/>.\n\n## Setup\n\n## Usage\n\n## Examples\n\nThere are two examples:\n\n- examples/static_joystick_example.py - show a column with a plot and the joystick, then exit.\n- examples/console_joystick_example.py - show a plot and the joystick in a bokeh server app. Callbacks from the front end drive console logs of the joystick position.\n\n## Roadmap\n\n- Get the example JS demo widget/bokeh model to work - whatever that widget is. - done\n- Figure out how to get values back to the python end with it. - done\n- Figure out how to swap their control for the joystick (however hacky) - done\n    - Note - this is a TS file from the original, adapted here. The DOM element change\n      is important.\n- Figure out how to make that tidier. - done\n- Figure out how to publish to PyPi (alpha) and test in a pip installed test.\n',
    'author': 'Danny Staple',
    'author_email': 'danny@orionrobots.co.uk',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
