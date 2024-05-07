# Bokeh Joystick Widget

This is a custom widget for the Python Bokeh library that allows you to control a joystick via mouse drags or touch gestures.

The widget has x and y properties that are updated as the joystick is moved. The x and y properties are in the range -100 to 100.

The widget is derived from <https://github.com/bobboteck/JoyStick/>.

## Setup

Install with pip:

```bash
pip install bokeh-joystick-widget
```

Or poetry:

```bash
poetry add bokeh-joystick-widget
```

## Usage

In your bokeh app, you can use the joystick widget like this:

```python
from bokeh_joystick_widget import JoystickWidget
:
# some plot
:
joystick = JoystickWidget()
joystick.on_change("position", lambda attr, old, new: print(f'x: {new["x"]}, y: {new["y"]}'))
:
:
show(column(joystick, plot))
```

## Examples

There are 3 examples:

- examples/static_joystick_example.py - show a column with a plot and the joystick, then exit.
- examples/console_joystick_example.py - show a plot and the joystick in a bokeh server app. Callbacks from the front end drive console logs of the joystick position.
- examples/bigger_joystick.py - Scale the size of the rendered joystick.

## Roadmap

- Get the example JS demo widget/bokeh model to work - whatever that widget is. - done
- Figure out how to get values back to the python end with it. - done
- Figure out how to swap their control for the joystick (however hacky) - done
    - Note - this is a TS file from the original, adapted here. The DOM element change
      is important.
- Figure out how to make that tidier. - done
- Figure out how to publish to PyPi (alpha) and test in a pip installed test. - done
