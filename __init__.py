# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTIBILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

bl_info = {
    "name": "XInput Reader",
    "author": "Erindale Woodford",
    "description": "Install and use the XInput library with a gamepad",
    "version": (0, 1),
    "blender": (3, 6, 0),
    "location": "View3D > Toolbar > XInput",
    "warning": "",
    "doc_url": "",
    "category": "3D View",
}

import bpy, os, sys, subprocess
try:
    import XInput
except:
    pass
from bpy.types import (Operator, Panel, AddonPreferences)   

#--------------------------------------------------------------------------------------------------------------------------------#
#----------------------------------------------------------PREFERENCES-----------------------------------------------------------#
#--------------------------------------------------------------------------------------------------------------------------------#

class XR_PT_preferences_panel(AddonPreferences):
    bl_idname = __package__

    def draw(self, context):
        layout = self.layout
        layout.operator("wm.install_xinput")
        layout.label(text="Might need to run Blender as Admin")
        layout.label(text="Check System Console for success/failure message")
        layout.label(text="Restart Blender after installing")

#------------------------------------------------------------------------------------------------------------------------------#
#----------------------------------------------------------FUNCTIONS-----------------------------------------------------------#
#------------------------------------------------------------------------------------------------------------------------------#


def get_reader():
    xinput_reader_empty = bpy.data.objects.get("XInput Reader")
    return xinput_reader_empty

def create_reader():
    xinput_reader_empty = bpy.data.objects.get("XInput Reader")
    if xinput_reader_empty is None:
        xinput_reader_empty = bpy.data.objects.new("XInput Reader", None)
        bpy.context.scene.collection.objects.link(xinput_reader_empty)
    return xinput_reader_empty



#------------------------------------------------------------------------------------------------------------------------------#
#----------------------------------------------------------OPERATORS-----------------------------------------------------------#
#------------------------------------------------------------------------------------------------------------------------------#


class XR_OT_install_xinput(Operator):
    bl_idname = "wm.install_xinput"
    bl_label = "Install XInput"
    bl_description = "Installs XInput"
    bl_options = {'REGISTER'}

    def execute(self, context):
        
        python_exe = os.path.join(sys.prefix, 'bin', 'python.exe') #windows
        if os.path.isfile(python_exe) is False:
            python_exe = os.path.join(sys.prefix, 'bin', 'python3.10') #linux & macOS
        target = os.path.join(sys.prefix, 'lib', 'site-packages')
        
        subprocess.call([python_exe, '-m', 'ensurepip'])
        subprocess.call([python_exe, '-m', 'pip', 'install', '--upgrade', 'pip'])
        subprocess.call([python_exe, '-m', 'pip', 'install', '--upgrade', 'Xinput-Python', '-t', target])
        return {'FINISHED'}

class XR_OT_monitor_controller(Operator):
    bl_idname = "wm.monitor_controller"
    bl_label = "Monitor Controller"
    bl_description = "Monitors controller input"
    bl_options = {'REGISTER'}

    _timer = None
    
    def modal(self, context, event):
        xinput_reader_empty = get_reader()

        if event.type in {'RIGHTMOUSE', 'ESC'}:
            self.cancel(context)
            xinput_reader_empty.location = xinput_reader_empty.location
            return {'CANCELLED'}
        

        #Controller inputs
        state = XInput.get_state(0)

        xinput_reader_empty["A"] = XInput.get_button_values(state)['A']
        xinput_reader_empty["B"] = XInput.get_button_values(state)['B']
        xinput_reader_empty["X"] = XInput.get_button_values(state)['X']
        xinput_reader_empty["Y"] = XInput.get_button_values(state)['Y']
        xinput_reader_empty["DPadUp"] = XInput.get_button_values(state)['DPAD_UP']
        xinput_reader_empty["DPadDown"] = XInput.get_button_values(state)['DPAD_DOWN']
        xinput_reader_empty["DPadLeft"] = XInput.get_button_values(state)['DPAD_LEFT']
        xinput_reader_empty["DPadRight"] = XInput.get_button_values(state)['DPAD_RIGHT']
        xinput_reader_empty["Start"] = XInput.get_button_values(state)['START']
        xinput_reader_empty["Back"] = XInput.get_button_values(state)['BACK']
        xinput_reader_empty["LeftThumb"] = XInput.get_button_values(state)['LEFT_THUMB']
        xinput_reader_empty["LeftThumbX"] = XInput.get_thumb_values(state)[0][0]
        xinput_reader_empty["LeftThumbY"] = XInput.get_thumb_values(state)[0][1]
        xinput_reader_empty["RightThumb"] = XInput.get_button_values(state)['RIGHT_THUMB']
        xinput_reader_empty["RightThumbX"] = XInput.get_thumb_values(state)[1][0]
        xinput_reader_empty["RightThumbY"] = XInput.get_thumb_values(state)[1][1]
        xinput_reader_empty["LeftShoulder"] = XInput.get_button_values(state)['LEFT_SHOULDER']
        xinput_reader_empty["RightShoulder"] = XInput.get_button_values(state)['RIGHT_SHOULDER']
        xinput_reader_empty["LeftTrigger"] = XInput.get_trigger_values(state)[0]
        xinput_reader_empty["RightTrigger"] = XInput.get_trigger_values(state)[1]
        
        # trigger scene update
        xinput_reader_empty.location = xinput_reader_empty.location
        return {'PASS_THROUGH'}
    
    def execute(self, context):
        try:
            import XInput
        except:
            self.report({'ERROR'}, "XInput not installed")
            return {'CANCELLED'}
        
        xinput_reader_empty = create_reader()

        wm = context.window_manager
        self._timer = wm.event_timer_add(0.1, window=context.window)
        wm.modal_handler_add(self)
        

        wm.modal_running = True
        return {'RUNNING_MODAL'}
    
    def cancel(self, context):
        wm = context.window_manager
        wm.event_timer_remove(self._timer)
        wm.modal_running = False


class XR_OT_drive_nodegroup(Operator):
    bl_idname = "wm.drive_nodegroup"
    bl_label = "Drive Nodegroup"
    bl_description = "Drive nodegroup from controller"
    bl_options = {'REGISTER'}

    def execute(self, context):
        xinput_reader_empty = get_reader()
        controller_inputs = xinput_reader_empty.items()

        xinput_nodegroup_name = 'XInput Reader'
        xinput_nodegroup = bpy.data.node_groups.get(xinput_nodegroup_name)

        #delete nodegroup if it exists
        if xinput_nodegroup is None:
            xinput_nodegroup = bpy.data.node_groups.new(xinput_nodegroup_name, 'GeometryNodeTree')
        
        #get output node
        output_node = None
        for node in xinput_nodegroup.nodes:
            if node.type == 'GROUP_OUTPUT':
                output_node = node
                break

        #create output node if none exists
        if output_node is None:
            output_node = xinput_nodegroup.nodes.new('NodeGroupOutput')
            output_node.location = (0, 0)

        for inputs in controller_inputs:
            if type(xinput_reader_empty[inputs[0]]) == float or int or bool:
                if inputs[0] not in xinput_nodegroup.outputs:
                    xinput_nodegroup.outputs.new("NodeSocketFloat", inputs[0])

                #set up driver
                output_socket = output_node.inputs[inputs[0]]
                fcurve = output_socket.driver_add('default_value')
                driver = fcurve.driver
                driver.type = 'AVERAGE'
                if len(driver.variables) == 0:
                    variable = driver.variables.new()
                else:
                    variable = driver.variables[0]
                variable.name = inputs[0]
                variable.type = 'SINGLE_PROP'
                targets = variable.targets[0]
                targets.id_type = 'OBJECT'
                targets.id = xinput_reader_empty
                targets.data_path = f'["{inputs[0]}"]'
                driver.expression = 'var'


        return {'FINISHED'}


#------------------------------------------------------------------------------------------------------------------------------#
#------------------------------------------------------------PANELS------------------------------------------------------------#
#------------------------------------------------------------------------------------------------------------------------------#


class XR_PT_panel(Panel):
    bl_label = "XInput Reader"
    bl_idname = "OBJECT_PT_XInput_panel"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "XInput"

    def draw(self, context):
        layout = self.layout
        col = layout.column()
        row = col.row()
        row.scale_y = 3
        if bpy.context.window_manager.modal_running == False:
            row.operator("wm.monitor_controller")
        else:
            row.operator("wm.monitor_controller", text="Right Click or Esc to Stop", icon="ERROR")
        col.separator()
        col.operator("wm.drive_nodegroup")

        xinput_reader_empty = get_reader()
        if xinput_reader_empty is not None:
            controller_inputs = xinput_reader_empty.items()

            box = layout.box()
            box.label(text="Controller Inputs")
            param_count = 0
            for controller_input in controller_inputs:
                if type(xinput_reader_empty[controller_input[0]]) == float or int or bool:
                    row = box.row()
                    prop_name = controller_input[0]
                    row.prop(xinput_reader_empty, f'["{prop_name}"]')
                    param_count += 1

#--------------------------------------------------------------------------------------------------------------------------------#
#------------------------------------------------------------REGISTER------------------------------------------------------------#
#--------------------------------------------------------------------------------------------------------------------------------#


classes = (
    XR_OT_install_xinput,
    XR_OT_monitor_controller,
    XR_OT_drive_nodegroup,
    XR_PT_panel,
    XR_PT_preferences_panel,
)

def register():
    bpy.types.WindowManager.modal_running = bpy.props.BoolProperty(default=False)

    from bpy.utils import register_class
    for cls in classes:
        register_class(cls)


def unregister():
    del bpy.types.WindowManager.modal_running

    from bpy.utils import unregister_class
    for cls in reversed(classes):
        unregister_class(cls)
