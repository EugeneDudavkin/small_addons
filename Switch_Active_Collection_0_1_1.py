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

import bpy
bl_info = {
    "name": "Switch Active Collection",
    "location": "3D View / Outliner",
    "version": (0, 1, 1),
    "blender": (2, 90, 0),
    "description": "Switching active Collection to the active Object selected",
    "author": "APEC",
    "category": "Object",
}

#Recursivly transverse layer_collection for a particular name
def recurLayerCollection(layerColl, collName):
    found = None
    if (layerColl.name == collName):
        return layerColl
    for layer in layerColl.children:
        found = recurLayerCollection(layer, collName)
        if found:
            return found

class OUTLINER_OT_switch_collection(bpy.types.Operator):
    """Makes an active collection where the active object is located"""
    bl_idname = "outliner.switch_collection"
    bl_label = "Switch Active Collection"
    #bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(self, context):
        ar = context.screen.areas
        __class__.area = next(
            (a for a in ar if a.type == 'OUTLINER'), None)
        return __class__.area

    def execute(self, context):
        obj = bpy.context.object
        ucol = obj.users_collection

        #Switching active Collection to active Object selected
        for i in ucol:
            layer_collection = bpy.context.view_layer.layer_collection
            layerColl = recurLayerCollection(layer_collection, i.name)
            bpy.context.view_layer.active_layer_collection = layerColl
        return {'FINISHED'}

def draw_sync_collection(self, context):
    self.layout.operator("outliner.switch_collection", text="", icon="FILE_TICK")

def register():
    bpy.types.OUTLINER_HT_header.append(draw_sync_collection)    
    bpy.utils.register_class(OUTLINER_OT_switch_collection)

def unregister():
    bpy.types.OUTLINER_HT_header.remove(draw_sync_collection)    
    bpy.utils.unregister_class(OUTLINER_OT_switch_collection)
