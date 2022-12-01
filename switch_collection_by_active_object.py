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
    "name": "Switch Collection by Active Object",
    "location": "3D View / Outliner",
    "version": (0, 1, 2),
    "blender": (2, 93, 0),
    "description": "Switching active Collection to the active Object selected",
    "author": "APEC",
    "category": "Outliner",
}

import bpy
from bpy.app.handlers import persistent

#Recursivly transverse layer_collection for a particular name
def recurLayerCollection(layerColl, collName):
    found = None
    if (layerColl.name == collName):
        return layerColl
    for layer in layerColl.children:
        found = recurLayerCollection(layer, collName)
        if found:
            return found

def msgbus_callback(*arg):
    switch_props = bpy.context.scene.SWITCH_PG_props
    
    if switch_props.olways_switch == True:
    
        # in console will be print active object name 
        print("Switching active collection to the object:", bpy.context.view_layer.objects.active.name)
    
        obj = bpy.context.object
        ucol = obj.users_collection

        #Switching active Collection to active Object selected
        for i in ucol:
            layer_collection = bpy.context.view_layer.layer_collection
            layerColl = recurLayerCollection(layer_collection, i.name)
            bpy.context.view_layer.active_layer_collection = layerColl

@persistent
def my_handler(context, a):
    subscribe_to_obj()

def subscribe_to_obj(): 
             
    bpy.msgbus.subscribe_rna(
        key=(bpy.types.LayerObjects, 'active'),
        owner=bpy,
        #args=('something, if you need',),
        args=(bpy.context,),
        notify=msgbus_callback,
        options={"PERSISTENT"}
    )
        

class SWITCH_PG_props(bpy.types.PropertyGroup):
    
    olways_switch: bpy.props.BoolProperty (
        name="Switch Collection", 
        default = False, 
        description="Always switch collection by active object"
    )
    

def draw_switch_collection(self, context):
    switch_props = context.scene.SWITCH_PG_props
    self.layout.prop(switch_props, "olways_switch", text="", icon="PLUGIN", toggle=True)

def register():
    bpy.types.OUTLINER_HT_header.append(draw_switch_collection)
    bpy.utils.register_class(SWITCH_PG_props)
    
    bpy.app.handlers.load_post.append(my_handler)

    bpy.types.Scene.SWITCH_PG_props = bpy.props.PointerProperty(type = SWITCH_PG_props)

def unregister():
    bpy.types.OUTLINER_HT_header.remove(draw_switch_collection)
    bpy.utils.unregister_class(SWITCH_PG_props)
    
    bpy.app.handlers.load_post.remove(my_handler)
    
    del bpy.types.Scene.SWITCH_PG_props
        
if __name__ == "__main__":
    register()
