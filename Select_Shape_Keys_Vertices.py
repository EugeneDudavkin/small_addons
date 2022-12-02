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
    "name": "Select vertices for active shape key",
    "author": "APEC",
    "version": (0, 0, 1),
    "blender": (2, 93, 0),
    "location": "Shape Keys > Shape Keys Specials",
    "description": "Select vertices for active shape key", 
    "doc_url": "",
    "tracker_url": "",      
    "category": "Mesh"
}

import bpy
from bpy.types import Operator

#https://blender.stackexchange.com/questions/116764/select-vertices-which-are-affected-by-a-shape-key
#https://blenderartists.org/t/getting-the-active-shape-key/618137

class SELECT_OT_shape_key_vertices(Operator):
    bl_idname = "select.shape_key_vertices"
    bl_label = "Select active shape vertices"
    bl_description = "Select vertices for active shape key"
    
#    @classmethod
#    def poll(cls, context):
#        # Checks to see if there's any active mesh object selected
#        active_object = context.active_object
#        return active_object is not None and active_object.type == 'MESH' and active_object.select_get()

    def execute(self, context):    
        tolerance = 1e-5
        obj = bpy.context.active_object
        #shape_keys = obj.data.shape_keys.key_blocks
        #sk1_data = shape_keys['Key 1'].data
        sk_active_data = obj.active_shape_key.data
        #skb_data = shape_keys['Basis'].data
        sk_base_data = obj.data.shape_keys.key_blocks[0].data

        bpy.ops.object.mode_set(mode="EDIT")
        bpy.ops.mesh.select_all(action="DESELECT")
        bpy.ops.mesh.select_mode(type="VERT")
        bpy.ops.object.mode_set(mode="OBJECT")

        for i, (x, y) in enumerate(zip(sk_active_data, sk_base_data)):
            if (x.co - y.co).length > tolerance:
                obj.data.vertices[i].select = True

        bpy.ops.object.mode_set(mode="EDIT")
        
        return {'FINISHED'}
    
###########################################################################################
#####################################    UI    ############################################
########################################################################################### 

def shape_key_specials_menu(self, context):
    obj = bpy.context.active_object
    sk_active_name = obj.active_shape_key.name
    sk_base_name = obj.data.shape_keys.key_blocks[0].name

    if sk_base_name != sk_active_name:
        layout = self.layout
        layout.separator()
        #layout.label(text="Select:")
        layout.operator("select.shape_key_vertices", icon="VERTEXSEL")
    
###########################################################################################
##################################### Register ############################################
########################################################################################### 	

def register():
    bpy.utils.register_class(SELECT_OT_shape_key_vertices)
    bpy.types.MESH_MT_shape_key_context_menu.append(shape_key_specials_menu)
    
def unregister():
    bpy.utils.unregister_class(SELECT_OT_shape_key_vertices)
    bpy.types.MESH_MT_shape_key_context_menu.remove(shape_key_specials_menu)
    
if __name__ == "__main__":
    register()