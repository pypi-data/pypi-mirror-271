from bokeh.models import InputWidget
from bokeh.core.properties import Bool, Float, Tuple, Int


class JoystickWidget(InputWidget):
    # This already picks up multiple ./ files imported by the TS.
    __implementation__ = "joystick_widget.ts"

    # Below are all the "properties" for this model. Bokeh properties are
    # class attributes that define the fields (and their types) that can be
    # communicated automatically between Python and the browser. Properties
    # also support type validation. More information about properties in
    # can be found here:
    #
    #    https://docs.bokeh.org/en/latest/docs/reference/core/properties.html#bokeh-core-properties

    auto_return_to_center = Bool(
        default=True, help="Return the joystick to center when released"
    )
    # Add properties that represent the joystick state
    position = Tuple(Float, Float, default=[0, 0], help="Position of the joystick")

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        if self.width is None:
            self.width = 200
        if self.height is None:
            self.height = 200
