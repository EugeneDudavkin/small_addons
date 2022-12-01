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
    "name": "Collection Visibility",
    "author": "APEC",
    "version": (0, 3, 1),
    "blender": (2, 93, 0),
    "location": "Outliner > Collections > RMB > Visibility",
    "description": "Change visibility for collection objects", 
    "doc_url": "",
    "tracker_url": "",      
    "category": "Outliner"
}

import bpy
from bpy.types import Operator

class COLLECTION_OT_visibility(Operator):    
    bl_idname = "collection.visibility"
    bl_label = "Collection Visibility"
    bl_description = '''Change visibility for collection objects'''
    bl_options = {'REGISTER', 'UNDO'}

    shading_type: bpy.props.EnumProperty (

    name="Shading Type", 

    items=[('BOUNDS','BOUNDS',''),
            ('SOLID','SOLID',''),
            ('TEXTURED','TEXTURED',''),
            ('WIRE','WIRE','')])

    def draw(self, context):
        layout = self.layout
        row = layout.row()
        row.prop(self, "shading_type", expand=True)

    def execute(self, context): 

        context = bpy.context
        ops = bpy.ops
        
        active_object = context.view_layer.objects.active
        objects_originals = context.selected_objects
        oldMode = bpy.context.object.mode
        
        if context.area.type == "OUTLINER":
            collection_names = [col.name for col in context.selected_ids]
            # use only collections whose names are in collection_names
            collections = [col for col in bpy.data.collections if col.name in collection_names]
            
            for col in collections:
                for obj in col.all_objects:
                    obj.select_set(True)
            
        if context.area.type == "VIEW_3D": 
            selection_names = [obj.name for obj in context.selected_objects]

            for o in selection_names:
                obj = bpy.context.scene.objects.get(o)
                bpy.context.view_layer.objects.active = obj
                obj.select_set(True)
                ops.object.select_grouped(extend=True, type='COLLECTION')                        
            
        selected_objects = context.selected_objects

        for obj in selected_objects:
            if self.shading_type == 'BOUNDS':
                obj.display_type = 'BOUNDS'
            if self.shading_type == 'SOLID':
                obj.display_type = 'SOLID'
            if self.shading_type == 'TEXTURED':
                obj.display_type = 'TEXTURED'
            if self.shading_type == 'WIRE':
                obj.display_type = 'WIRE'        
                
        bpy.ops.object.mode_set(mode='OBJECT')
        ops.object.select_all(action='DESELECT')
        
        # selecting original objects with active
        for obj in objects_originals:
            obj.select_set(True)
        context.view_layer.objects.active = active_object
        active_object.select_set(True)
        
        bpy.ops.object.mode_set(mode=oldMode)
        
        return { 'FINISHED' } 


class OBJECT_OT_collection_wire_toggle(Operator):    
    bl_idname = "object.collection_wire_toggle"
    bl_label = "Toggle collection by object wire/textured"
    bl_description = '''Change visibility for all objects in collections'''

    def execute(self, context):
        context = bpy.context
        ops = bpy.ops
        context.view_layer.objects.active.select_set(True) 
        active_object = context.view_layer.objects.active
        objects_originals = context.selected_objects
        oldMode = bpy.context.object.mode

#        active_object.select_set(True)

        selection_names = [obj.name for obj in context.selected_objects]
#        if context.area.type == "OUTLINER":
        for o in selection_names:
            obj = context.scene.objects.get(o)
            context.view_layer.objects.active = obj
            obj.select_set(True)
            ops.object.select_grouped(extend=True, type='COLLECTION')
    
        selected_objects = context.selected_objects

        if active_object.display_type != 'WIRE':
            for obj in selected_objects:
                obj.display_type = 'WIRE'
        else:
            for obj in selected_objects:
                obj.display_type = 'TEXTURED'
                      
        bpy.ops.object.mode_set(mode='OBJECT')
        ops.object.select_all(action='DESELECT')

        # selecting original objects with active
        for obj in objects_originals:
            obj.select_set(True)
        context.view_layer.objects.active = active_object
        active_object.select_set(True)
        
        bpy.ops.object.mode_set(mode=oldMode)
        
        return { 'FINISHED' }
        

class OBJECT_OT_collection_bounds_toggle(Operator):    
    bl_idname = "object.collection_bounds_toggle"
    bl_label = "Toggle collection by object bounds/textured"
    bl_description = '''Change visibility for all objects in collections'''

    def execute(self, context):
        context = bpy.context
        ops = bpy.ops
        context.view_layer.objects.active.select_set(True) 
        active_object = context.view_layer.objects.active
        objects_originals = context.selected_objects
        oldMode = bpy.context.object.mode
        
#        active_object.select_set(True)

        selection_names = [obj.name for obj in context.selected_objects]
#        if context.area.type == "OUTLINER":
        for o in selection_names:
            obj = context.scene.objects.get(o)
            context.view_layer.objects.active = obj
            obj.select_set(True)
            ops.object.select_grouped(extend=True, type='COLLECTION')
    
        selected_objects = context.selected_objects

        if active_object.display_type != 'BOUNDS':
            for obj in selected_objects:
                obj.display_type = 'BOUNDS'
        else:
            for obj in selected_objects:
                obj.display_type = 'TEXTURED'
                      
        bpy.ops.object.mode_set(mode='OBJECT')
        ops.object.select_all(action='DESELECT')

        # selecting original objects with active
        for obj in objects_originals:
            obj.select_set(True)
        context.view_layer.objects.active = active_object
        active_object.select_set(True)
        
        bpy.ops.object.mode_set(mode=oldMode)
        
        return { 'FINISHED' }
        

class OBJECT_OT_wire_toggle(Operator):    
    bl_idname = "object.wire_toggle"
    bl_label = "Toggle objects by active object wire/textured"
    bl_description = '''Change visibility for objects'''

    def execute(self, context):
        context = bpy.context
        ops = bpy.ops
        context.view_layer.objects.active.select_set(True)
        active_object = context.view_layer.objects.active
        objects_originals = context.selected_objects
        oldMode = bpy.context.object.mode

#        active_object.select_set(True)

        if active_object.display_type != 'WIRE':
            for obj in objects_originals:
                obj.display_type = 'WIRE'
        else:
            for obj in objects_originals:
                obj.display_type = 'TEXTURED'
                      
        bpy.ops.object.mode_set(mode='OBJECT')
        ops.object.select_all(action='DESELECT')

        # selecting original objects with active
        for obj in objects_originals:
            obj.select_set(True)
        context.view_layer.objects.active = active_object
        active_object.select_set(True)
        
        bpy.ops.object.mode_set(mode=oldMode)
        
        return { 'FINISHED' }
        

class OBJECT_OT_bounds_toggle(Operator):    
    bl_idname = "object.bounds_toggle"
    bl_label = "Toggle objects by active object bounds/textured"
    bl_description = '''Change visibility for objects'''

    def execute(self, context):
        context = bpy.context
        ops = bpy.ops
        context.view_layer.objects.active.select_set(True) 
        active_object = context.view_layer.objects.active
        objects_originals = context.selected_objects
        oldMode = bpy.context.object.mode
        
        active_object.select_set(True)

        if active_object.display_type != 'BOUNDS':
            for obj in objects_originals:
                obj.display_type = 'BOUNDS'
        else:
            for obj in objects_originals:
                obj.display_type = 'TEXTURED'
                      
        bpy.ops.object.mode_set(mode='OBJECT')
        ops.object.select_all(action='DESELECT')

        # selecting original objects with active
        for obj in objects_originals:
            obj.select_set(True)
        context.view_layer.objects.active = active_object
        active_object.select_set(True)
        
        bpy.ops.object.mode_set(mode=oldMode)
        
        return { 'FINISHED' }
###########################################################################################
#####################################    UI    ############################################
########################################################################################### 

def select_colection_obects_menu_outliner(self, context):
    layout = self.layout
    layout.separator()
    layout.label(text="Show as:")
    layout.operator(COLLECTION_OT_visibility.bl_idname, text="BOUNDS", icon='CUBE').shading_type = 'BOUNDS'
    layout.operator(COLLECTION_OT_visibility.bl_idname, text="SOLID", icon='SHADING_SOLID').shading_type = 'SOLID'
    layout.operator(COLLECTION_OT_visibility.bl_idname, text="TEXTURED", icon='UV_DATA').shading_type = 'TEXTURED'
    layout.operator(COLLECTION_OT_visibility.bl_idname, text="WIRE", icon='SHADING_WIRE').shading_type = 'WIRE'
   
###########################################################################################
##################################### Register ############################################
########################################################################################### 	

def register():
    bpy.utils.register_class(OBJECT_OT_collection_wire_toggle)
    bpy.utils.register_class(OBJECT_OT_collection_bounds_toggle)
    bpy.utils.register_class(OBJECT_OT_wire_toggle)
    bpy.utils.register_class(OBJECT_OT_bounds_toggle)
    bpy.utils.register_class(COLLECTION_OT_visibility)
    bpy.types.OUTLINER_MT_collection_visibility.append(select_colection_obects_menu_outliner)
    
def unregister():
    bpy.utils.unregister_class(OBJECT_OT_collection_wire_toggle)
    bpy.utils.unregister_class(OBJECT_OT_collection_bounds_toggle)
    bpy.utils.unregister_class(OBJECT_OT_wire_toggle)
    bpy.utils.unregister_class(OBJECT_OT_bounds_toggle)
    bpy.utils.unregister_class(COLLECTION_OT_visibility)
    bpy.types.OUTLINER_MT_collection_visibility.remove(select_colection_obects_menu_outliner)
    
if __name__ == "__main__":
    register()