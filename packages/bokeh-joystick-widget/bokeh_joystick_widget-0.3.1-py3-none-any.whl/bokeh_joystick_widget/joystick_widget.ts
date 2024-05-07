// The "core/properties" module has all the property types
import * as p from "core/properties"

// HTML construction and manipulation functions
import { div } from "core/dom"

// We will subclass in JavaScript from the same class that was subclassed
// from in Python
import { Widget, WidgetView } from "models/widgets/widget"
import { JoyStick } from "./joystick"


export class JoystickWidgetView extends WidgetView {
  declare model: JoystickWidget;
  theJoystick: any;
  joy_el!: HTMLElement;



  override connect_signals(): void {
    super.connect_signals();
    // Connect signals here, for example, to listen for changes to model properties
  }

  override render(): void {
      super.render()

      this.joy_el = div({id: 'joyDiv', style: {width: this.model.width + 'px', height: this.model.height + 'px'}})
      this.shadow_el.appendChild(this.joy_el)
      this.model.position = [0, 0]

      // // Add event listener for Bokeh's "after_layout" event
      // this.connect(this.model.layout, 'after_layout', () => {
      //     // DOM element is now available
      //     this.init_joystick()
      // })
  }

  override after_layout(): void {
      // Initialize the joystick
      this.theJoystick = new JoyStick(
        this.joy_el, {
          autoReturnToCenter: this.model.auto_return_to_center
        }, (stickData: any) => this.position_changed(stickData)
      )
  }

  position_changed(stickData: any): void {
      // Do something when the position changes
      this.model.position = [stickData.x, stickData.y]
  }
}

export namespace JoystickWidget {
  export type Attrs = p.AttrsOf<Props>

  export type Props = Widget.Props & {
    position: p.Property<[number, number] | null>
    auto_return_to_center: p.Property<boolean>
  }
}

export interface JoystickWidget extends JoystickWidget.Attrs {};

export class JoystickWidget extends Widget {
  declare properties: JoystickWidget.Props;
  declare __view_type__: JoystickWidgetView;

  constructor(attrs?: Partial<JoystickWidget.Attrs>) {
    super(attrs)
  }

  static {
    this.prototype.default_view = JoystickWidgetView;

    this.define<JoystickWidget.Props>(({Tuple, Bool, Float, Nullable}) => ({
      position: [ Nullable(Tuple(Float, Float)), null ],
      auto_return_to_center: [Bool, true]
    }))
  }
}
