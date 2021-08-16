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
    "name": "Cameras List",
    "author": "APEC",
    "version": (0, 1, 0),
    "blender": (2, 93, 0),
    "location": "View3d > RMB > Active Camera",
    "description": "Menu with scene cameras", 
    "doc_url": "",
    "tracker_url": "",      
    "category": "3D View"
}

import bpy


class VIEW3D_MT_cameras_main(bpy.types.Menu):
    """Main menu for scene Cameras"""

    bl_idname = "VIEW3D_MT_cameras_main"
    bl_label = "Active Camera"

    def draw(self, context):
        layout = self.layout        
        layout.prop(bpy.context.scene, "camera", text="", icon="CAMERA_DATA")

        #layout.separator()

###########################################################################################
#####################################    UI    ############################################
########################################################################################### 

def cameras_specials_menu(self, contxt):
    ob = bpy.context.object
    if ob is not None and ob.type == 'CAMERA':
        self.layout.separator()
        self.layout.menu(VIEW3D_MT_cameras_main.bl_idname, icon="VIEW_CAMERA")
   
###########################################################################################
##################################### Register ############################################
########################################################################################### 	

def register():
    bpy.utils.register_class(VIEW3D_MT_cameras_main)
    bpy.types.VIEW3D_MT_object_context_menu.prepend(cameras_specials_menu)
    #bpy.types.VIEW3D_MT_object_context_menu.append(cameras_specials_menu)
    
def unregister():
    bpy.utils.unregister_class(VIEW3D_MT_cameras_main)
    bpy.types.VIEW3D_MT_object_context_menu.remove(cameras_specials_menu)
    
if __name__ == "__main__":
    register()