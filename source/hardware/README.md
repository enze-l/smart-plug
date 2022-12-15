# Hardware

This module is used to access all the hardware of the plug. It is handed over as a parameter to every API that runs on this plug and abstracts the technical details of the hardware. The following components are provided:

- led
- relay
- button_internal
- button_external

As an example for the usage of the module we turn on a led:

```hardware.led.turn_on()```

Accessing information works similar. With the following call we can figure out the state of the led:

```hardware.led.get_on_state()```

## Components
### LED & RELAY
Both of these components can be accessed via ```hardware.led``` and ```hardware.relay``` respectively.

They both provide the same functionality and offer the following methods. To reduce redundancy the led is used for the examples:

#### Methods:
Turn consumer on:
```
led.turn_on()
```
Turn consumer off:
```
led.turn_off()
```
Toggle the state of the consumer:
```
led.toggle()
```
Set the state of the consumer:
```
led.set_on_state(True)
```
Get the state of the consumer:
```
led.get_on_state()  //True
```

### Internal_Button & External_Button
The [reference hardware](https://www.shelly.cloud/de/products/product-overview/2xspl1pm/shelly-plus-1-pm) has a built-in button. Furthermore, there is an option to wire up another button via designated contacts at the screw terminals.

To be able to use them you can provide them with functions to call if they are activated.

The following demonstrates how to print a "Hello World" if the internal button is pressed and released again:
```
def print_hello_world():
    print("Hello World!")
    
hardware.internal_button.set_on_release_function(print_hello_world)
```

The ```set_on_release_function``` should be sufficient for most use cases.

Unfortunately there are two different kind of buttons. On the one side there are buttons like the built-in button of the [reference hardware](https://www.shelly.cloud/de/products/product-overview/2xspl1pm/shelly-plus-1-pm), smartphone-power-buttons and keyboards. These are in an off state and transition into an on state when they are pressed. Once they are released, they go back into the off state. On the other side there are buttons like many light-switches that have two distinct states: one on-state and one off-state. To not confuse both kind of buttons, we will call the first kind of button "momentary button" and the second kind "toggle button". The reason for this detailed explanation is that the plug can't recognize which kind of button is connected to it, and it's up to the user to choose the right way for implementing its functionality.

#### Methods
Execute the given method if the momentary button is getting clicked / the toggle button is switched to one state.
```
external_button.set_on_click_function(my_function)
```
Execute the given method if the momentary button is released / the toggle button is switched to its other state.
```
external_button.set_on_release_function(my_function)
```
Execute the given method if the momentary button is pressed or released / the toggle button is switched to either state.
```
external_button.set_on_toggle_function(my_function)
```

