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

#https://blender.stackexchange.com/questions/64951/add-menu-entry-to-generic-right-click-menu
#https://stackoverflow.com/questions/27265915/get-list-of-selected-objects-as-string-blender-python
#https://blender.stackexchange.com/questions/132825/python-selecting-object-by-name-in-2-8/132829
#https://blenderartists.org/t/python-scripted-button-select-hierarchy-parent-and-children-at-same-time/1132109/4

# Add-on info
bl_info = {
    "name": "Outliner Menu Entries",
    "author": "APEC",
    "version": (0, 1, 0),
    "blender": (2, 92, 0),
    "location": "Outliner > Objects RMB or Collections RMB",
    "description": "Adds menu entries for objects and collections in Outliner", 
    "doc_url": "",
    "tracker_url": "",      
    "category": "Outliner"
}

import bpy
from bpy.types import Operator
from collections import  defaultdict

###########################################################################################
################################### Functions #############################################
###########################################################################################

class OUTLINER_OT_duplicate(Operator):    
    bl_idname = "outliner.duplicate"
    bl_label = "Duplicate"
    bl_description = '''Duplicate selected objects'''
    bl_options = { 'REGISTER', 'UNDO' }

    def execute(self, context):
        bpy.ops.object.mode_set(mode = 'OBJECT')    
        bpy.ops.object.duplicate()
        #dupli_obj = bpy.context.object
                
        return { 'FINISHED' }   

class OUTLINER_OT_duplicate_hierarchy(Operator):    
    bl_idname = "outliner.duplicate_hierarchy"
    bl_label = "Duplicate Hierarchy"
    bl_description = '''Duplicate selected objects with respecting the hierarchy'''
    bl_options = { 'REGISTER', 'UNDO' }

    def execute(self, context):   
        bpy.ops.object.mode_set(mode = 'OBJECT')

        selection_names = [obj.name for obj in bpy.context.selected_objects]

        for o in selection_names:
            obj = bpy.context.scene.objects.get(o)
            bpy.context.view_layer.objects.active = obj
            obj.select_set(True)
            bpy.ops.object.select_grouped(extend=True, type='CHILDREN_RECURSIVE')

        bpy.ops.object.duplicate()
        
        return { 'FINISHED' } 

class OUTLINER_OT_duplicate_instance(Operator):    
    bl_idname = "outliner.duplicate_instance"
    bl_label = "Duplicate Instance"
    bl_description = '''Duplicate selected objects with instances'''
    bl_options = { 'REGISTER', 'UNDO' }

    def execute(self, context):   
        bpy.ops.object.mode_set(mode = 'OBJECT')
        bpy.ops.object.duplicate(linked=True)
        #dupli_obj = bpy.context.object
                
        return { 'FINISHED' } 

class OUTLINER_OT_duplicate_instance_hierarchy(Operator):    
    bl_idname = "outliner.duplicate_instance_hierarchy"
    bl_label = "Duplicate Instance Hierarchy"
    bl_description = '''Duplicate selected objects with instances respecting the hierarchy'''
    bl_options = { 'REGISTER', 'UNDO' }

    def execute(self, context):
        bpy.ops.object.mode_set(mode = 'OBJECT')

        selection_names = [obj.name for obj in bpy.context.selected_objects]

        for o in selection_names:
            obj = bpy.context.scene.objects.get(o)
            bpy.context.view_layer.objects.active = obj
            obj.select_set(True)
            bpy.ops.object.select_grouped(extend=True, type='CHILDREN_RECURSIVE')

        bpy.ops.object.duplicate(linked=True)

        return { 'FINISHED' } 

class OUTLINER_OT_select_hierarchy(Operator):    
    bl_idname = "outliner.select_hierarchy"
    bl_label = "Select Hierarchy Multi"
    bl_description = '''Selects hierarchy and parent for multiple objects'''
    bl_options = { 'REGISTER', 'UNDO' }

    def execute(self, context):   
        bpy.ops.object.mode_set(mode = 'OBJECT')

        selection_names = [obj.name for obj in bpy.context.selected_objects]

        for o in selection_names:
            obj = bpy.context.scene.objects.get(o)
            bpy.context.view_layer.objects.active = obj
            obj.select_set(True)
            bpy.ops.object.select_grouped(extend=True, type='CHILDREN_RECURSIVE')
    
        return { 'FINISHED' } 

#https://blenderartists.org/t/how-to-select-all-objects-of-a-known-collection-with-python/1195742/3
class OUTLINER_OT_select_collection_objects(Operator):    
    bl_idname = "outliner.select_collection_objects"
    bl_label = "Select Objects Multi"
    bl_description = '''Selects all objects for multiple collections'''
    bl_options = { 'REGISTER', 'UNDO' }

    def execute(self, context): 

        collection_names = [col.name for col in bpy.context.selected_ids]

        # use only collections whose names are in collection_names
        collections = [col for col in bpy.data.collections if col.name in collection_names]

        for col in collections:
            for obj in col.all_objects:
                obj.select_set(True)
    
        return { 'FINISHED' } 


def copy_objects(from_col, to_col, linked, dupe_lut):
    for o in from_col.objects:
        dupe = o.copy()
        if not linked and o.data:
            dupe.data = dupe.data.copy()
        to_col.objects.link(dupe)
        dupe_lut[o] = dupe

def copy(parent, collection, linked=False):
    dupe_lut = defaultdict(lambda : None)
    def _copy(parent, collection, linked=False):
        cc = bpy.data.collections.new(collection.name)
        copy_objects(collection, cc, linked, dupe_lut)

        for c in collection.children:
            _copy(cc, c, linked)

        parent.children.link(cc)
    
    _copy(parent, collection, linked)
    print(dupe_lut)
    for o, dupe in tuple(dupe_lut.items()):
        parent = dupe_lut[o.parent]
        if parent:
            dupe.parent = parent

#https://blender.stackexchange.com/questions/157828/python-collection-duplicate-help
class OUTLINER_OT_duplicate_collections(Operator):    
    bl_idname = "outliner.duplicate_collections"
    bl_label = "Duplicate Collection Multi"
    bl_description = '''Duplicate multiple selected collections'''
    bl_options = { 'REGISTER', 'UNDO' }

    def execute(self, context): 

        context = bpy.context
        scene = context.scene

        collection_names = [col.name for col in bpy.context.selected_ids]

        for col_name in collection_names:
            col = bpy.data.collections.get(col_name)
            print(col, scene.collection)
            assert(col is not scene.collection)
            parent_col = context.scene.collection

            copy(scene.collection, col)
            # and linked copy
            #copy(scene.collection, col, linked=True)
                        
        return { 'FINISHED' } 

class OUTLINER_OT_duplicate_collections_linked(Operator):    
    bl_idname = "outliner.duplicate_collections_linked"
    bl_label = "Duplicate Linked Multi"
    bl_description = '''Duplicate multiple selected collections with linked object data'''
    bl_options = { 'REGISTER', 'UNDO' }

    def execute(self, context): 

        context = bpy.context
        scene = context.scene

        collection_names = [col.name for col in bpy.context.selected_ids]

        for col_name in collection_names:
            col = bpy.data.collections.get(col_name)
            print(col, scene.collection)
            assert(col is not scene.collection)
            parent_col = context.scene.collection

            copy(scene.collection, col, linked=True)
                        
        return { 'FINISHED' }         
###########################################################################################
#####################################    UI    ############################################
########################################################################################### 

def duplicate_menu_outliner(self, context):
    layout = self.layout
    layout.separator()
    layout.operator(OUTLINER_OT_duplicate.bl_idname)
    layout.operator(OUTLINER_OT_duplicate_hierarchy.bl_idname)
    layout.separator()
    layout.operator(OUTLINER_OT_duplicate_instance.bl_idname)
    layout.operator(OUTLINER_OT_duplicate_instance_hierarchy.bl_idname)
    layout.separator()
    layout.operator(OUTLINER_OT_select_hierarchy.bl_idname)

def select_colection_obects_menu_outliner(self, context):
    layout = self.layout
    layout.separator()
    layout.operator(OUTLINER_OT_duplicate_collections.bl_idname)
    layout.operator(OUTLINER_OT_duplicate_collections_linked.bl_idname)
    layout.separator()
    layout.operator(OUTLINER_OT_select_collection_objects.bl_idname)
   
###########################################################################################
##################################### Register ############################################
########################################################################################### 	

def register():
    bpy.utils.register_class(OUTLINER_OT_duplicate)
    bpy.utils.register_class(OUTLINER_OT_duplicate_hierarchy)
    bpy.utils.register_class(OUTLINER_OT_duplicate_instance)
    bpy.utils.register_class(OUTLINER_OT_duplicate_instance_hierarchy)
    bpy.utils.register_class(OUTLINER_OT_select_hierarchy)
    bpy.types.OUTLINER_MT_object.append(duplicate_menu_outliner)
    
    bpy.utils.register_class(OUTLINER_OT_select_collection_objects)
    bpy.utils.register_class(OUTLINER_OT_duplicate_collections)
    bpy.utils.register_class(OUTLINER_OT_duplicate_collections_linked)
    bpy.types.OUTLINER_MT_collection.append(select_colection_obects_menu_outliner)
    
def unregister():
    bpy.utils.unregister_class(OUTLINER_OT_duplicate)
    bpy.utils.unregister_class(OUTLINER_OT_duplicate_hierarchy)
    bpy.utils.unregister_class(OUTLINER_OT_duplicate_instance)
    bpy.utils.unregister_class(OUTLINER_OT_duplicate_instance_hierarchy)
    bpy.utils.unregister_class(OUTLINER_OT_select_hierarchy)
    bpy.types.OUTLINER_MT_object.remove(duplicate_menu_outliner)
    
    bpy.utils.unregister_class(OUTLINER_OT_select_collection_objects)
    bpy.utils.unregister_class(OUTLINER_OT_duplicate_collections)
    bpy.utils.unregister_class(OUTLINER_OT_duplicate_collections_linked)
    bpy.types.OUTLINER_MT_collection.remove(select_colection_obects_menu_outliner)
    
if __name__ == "__main__":
    register()
