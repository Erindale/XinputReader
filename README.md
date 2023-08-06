# XinputReader
Use XInput python library with Blender for gamepad controls!

The add-on is made to work with an XBox style gamepad and some minor alteration might be needed if the relevant buttons are not found on your controller.

One button triggers the creation of an empty object with custom properties matching the button inputs. These can be used as drivers for any type of control within Blender.

There is a second button that creates a geometry nodes group and sets up drivers to all the sockets so it can be used as an easy control hub.

This add-on is **not** heavily tested but you're welcome to fork and adjust as required!

# Installation

Install the XInput library via pip using the button in the add-on preferences.
Toggle system console to check if it succeeded or errored. If you see a lot of red, you'll need to run Blender as an administrator.
If you still see red, try downloading a portable version of Blender.

I can't promise this will install on all systems. You might need to manually install the XInput library if permissions don't work for you. I couldn't make the Windows Store install properly on Win11, nor could I get the Snap Store version to install on Fedora 38 linux. I have not tested on Mac.

Runs as a modal operator so take care with the lack of auto-saves!!

Good luck!