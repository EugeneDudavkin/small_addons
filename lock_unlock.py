# ##### BEGIN GPL LICENSE BLOCK #####
#
#  This program is free software; you can redistribute it and/or
#  modify it under the terms of the GNU General Public License
#  as published by the Free Software Foundation; either version 2
#  of the License, or (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software Foundation,
#  Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA.
#
# ##### END GPL LICENSE BLOCK #####

# Add-on info
bl_info = {
    "name": "Lock / Unlock Objects",
    "author": "APEC",
    "version": (0, 1, 0),
    "blender": (2, 93, 0),
    "location": "View3d",
    "description": "Simple operator to lock/unlock objects", 
    "doc_url": "",
    "tracker_url": "",      
    "category": "3D View"
}

import bpy

class LOCK_OT_unlock(bpy.types.Operator):
    bl_idname = "objects.lock_unlock"
    bl_label = "Lock/Unlock objects"
    bl_description = ""
    #bl_options = {"REGISTER", "UNDO"}

    action: bpy.props.EnumProperty (
            items=[('lock','lock',''),
                    ('unlock','unlock','')]
    )

#    def draw(self, context):
#        layout = self.layout
#        cbox.operator("objects.lock_unlock", text = "Lock objects").action = "lock"
#        cbox.operator("objects.lock_unlock", text = "Unlock objects").action = "unlock"
    
    def execute(self, context):
        if self.action == "lock":
            sel_obj = bpy.context.selected_objects
            for o in sel_obj:
                o.hide_select = True

        if self.action == "unlock":
            objects = bpy.context.scene.objects
            for o in objects:
                o.hide_select = False
        
        return {'FINISHED'}
    
def register():
    bpy.utils.register_class(LOCK_OT_unlock)
    
def unregister():
    bpy.utils.unregister_class(LOCK_OT_unlock)
    
if __name__ == "__main__":
    register()
