# XinputReader
Use XInput python library with Blender for gamepad controls in **Windows**!

The add-on is made to work with an XBox style gamepad and some minor alteration might be needed if the relevant buttons are not found on your controller.

One button triggers the creation of an empty object with custom properties matching the button inputs. These can be used as drivers for any type of control within Blender.

There is a second button that creates a geometry nodes group and sets up drivers to all the sockets so it can be used as an easy control hub.

This add-on is **not** heavily tested but you're welcome to fork and adjust as required!

# Installation

~~Install the XInput library via pip using the button in the add-on preferences.
Toggle system console to check if it succeeded or errored. If you see a lot of red, you'll need to run Blender as an administrator.
If you still see red, try downloading a portable version of Blender.~~

(Following 4.2 extension conventions, the python wheel is now bundled)

Runs as a modal operator so take care with the lack of auto-saves!!

Good luck!
