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
    "name": "Precision Scaler",
    "author": "APEC",
    "version": (0, 1, 1),
    "blender": (2, 93, 0),
    "location": "View3d > N-Panel > PreScaler",
    "description": "Scale selected by defined length", 
    "doc_url": "",
    "tracker_url": "",      
    "category": "Mesh"
}

import bpy
import bmesh
from bpy.types import Operator, PropertyGroup, Panel, AddonPreferences

def get_float1(self):
    scale_props = bpy.context.scene.PRESCALE_PG_props
    return scale_props.default_first
    
def set_float1(self, value):
    scale_props = bpy.context.scene.PRESCALE_PG_props
    scale_props.default_first = value

def get_float2(self):
    scale_props = bpy.context.scene.PRESCALE_PG_props
    return scale_props.default_second

def set_float2(self, value):
    scale_props = bpy.context.scene.PRESCALE_PG_props
    scale_props.default_second = value

def distance_between():
    active_object = bpy.context.active_object
    selected_objects = bpy.context.selected_objects
    
    if active_object and active_object.type == 'MESH' and bpy.context.mode == 'EDIT_MESH': 
        obj = bpy.context.edit_object
        me = obj.data
        bm = bmesh.from_edit_mesh(me)

        elem_list = []

        for g in bm.select_history:
            elem_list.append(g)
            
        if len(elem_list) == 2:
            point_first  = elem_list[0].co
            point_second = elem_list[1].co

            distance = (point_second - point_first).length
        
    if len(selected_objects) == 2:
        if active_object and active_object.type == 'MESH' and bpy.context.mode == 'OBJECT':
            obj1 = selected_objects[0].matrix_world.to_translation()
            obj2 = selected_objects[1].matrix_world.to_translation()

            distance = (obj1 - obj2).length
        
    return distance


class PRESCALE_OT_operator(Operator):
    bl_idname = "precision.scaler"
    bl_label = "Precision Scaler"
    bl_description = "Scale = Set / Get"

    action: bpy.props.EnumProperty (
        items=[('GET','GET',''),
               ('SET','SET',''),
               ('SCALE','SCALE','')])
               
    def execute(self, context):
        scale_props = context.scene.PRESCALE_PG_props        
        active_object = context.active_object
        current_mode = bpy.context.object.mode
                
        if self.action == "GET":
            try:
                scale_props.l1 = distance_between() 
            except:
                if bpy.context.mode == 'EDIT_MESH':
                    self.report({'WARNING'}, 'Need to click on first and second vertices')                    
                if bpy.context.mode == 'OBJECT':
                    self.report({'WARNING'}, 'Need to select two objects')
                return {'CANCELLED'}
                
        if self.action == "SET":
            try:
                scale_props.l2 = distance_between()
            except:
                if bpy.context.mode == 'EDIT_MESH':
                    self.report({'WARNING'}, 'Need to click on first and second vertices')
                if bpy.context.mode == 'OBJECT':
                    self.report({'WARNING'}, 'Need to select two objects')
                return {'CANCELLED'}

#            if self.action == "SCALE":                    
#                real_cursor = bpy.context.scene.cursor.matrix
#                real_transform = bpy.context.scene.transform_orientation_slots[0].type
#                real_pivot = bpy.context.scene.tool_settings.transform_pivot_point 
            
#                bpy.context.scene.cursor.matrix = bpy.context.object.matrix_world
#                obj_origin = bpy.context.scene.cursor.matrix
            
#                if scale_props.selection_only == True:  
#                    bpy.ops.object.mode_set(mode='EDIT') 
                
#                if scale_props.selection_only == False:  
#                    bpy.ops.object.mode_set(mode='OBJECT')            
            
#                if scale_props.use_cursor == True:
#                    bpy.context.scene.cursor.matrix = real_cursor
#                    bpy.context.scene.transform_orientation_slots[0].type = 'CURSOR'
#                    bpy.context.scene.tool_settings.transform_pivot_point = 'CURSOR'

#                    if scale_props.selection_only == False: 
#                        bpy.context.scene.tool_settings.use_transform_data_origin = True
#                        bpy.ops.object.origin_set(type='ORIGIN_CURSOR', center='MEDIAN')                
#                        bpy.ops.transform.transform(mode='ALIGN', orient_type='CURSOR')
#                        bpy.context.scene.tool_settings.use_transform_data_origin = False           
            
#                scale = scale_props.l2 / scale_props.l1      
            
#                if scale_props.use_x == True:
#                    x = scale
            
#                if scale_props.use_x == False:
#                    x = 1
            
#                if scale_props.use_y == True:
#                    y = scale
            
#                if scale_props.use_y == False:
#                    y = 1
            
#                if scale_props.use_z == True:
#                    z = scale
            
#                if scale_props.use_z == False:
#                    z = 1
                
#                bpy.ops.transform.resize(value=(x, y, z))                
            
#                bpy.context.scene.transform_orientation_slots[0].type = real_transform
#                bpy.context.scene.tool_settings.transform_pivot_point = real_pivot
            
#                if scale_props.selection_only == False:
#                    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)            
#                    bpy.context.scene.cursor.matrix = obj_origin
#                    bpy.context.scene.tool_settings.use_transform_data_origin = True
#                    bpy.ops.object.origin_set(type='ORIGIN_CURSOR', center='MEDIAN')            
#                    bpy.ops.transform.transform(mode='ALIGN', orient_type='CURSOR')
#                    bpy.context.scene.tool_settings.use_transform_data_origin = False
            
#                bpy.context.scene.cursor.matrix = real_cursor

#                bpy.ops.object.mode_set(mode='EDIT')
        
        if self.action == "SCALE":                    
            real_transform = bpy.context.scene.transform_orientation_slots[0].type
            real_pivot = bpy.context.scene.tool_settings.transform_pivot_point
            
            if scale_props.selection_only == True:
                bpy.ops.object.mode_set(mode='EDIT') 
                
            if scale_props.selection_only == False:
                bpy.ops.object.mode_set(mode='OBJECT')
            
            if scale_props.use_cursor == True:
                bpy.context.scene.transform_orientation_slots[0].type = 'CURSOR'
                bpy.context.scene.tool_settings.transform_pivot_point = 'CURSOR'
                            
            scale = scale_props.l2 / scale_props.l1      
            
            if scale_props.use_x == True:
                x = scale
            
            if scale_props.use_x == False:
                x = 1
            
            if scale_props.use_y == True:
                y = scale
            
            if scale_props.use_y == False:
                y = 1
            
            if scale_props.use_z == True:
                z = scale
            
            if scale_props.use_z == False:
                z = 1
                
            bpy.ops.transform.resize(value=(x, y, z))                
            
            bpy.context.scene.transform_orientation_slots[0].type = real_transform
            bpy.context.scene.tool_settings.transform_pivot_point = real_pivot
            
            if scale_props.selection_only == False:
                bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)  

            #bpy.ops.object.mode_set(mode='EDIT')
            bpy.ops.object.mode_set(mode=current_mode)

#        print("----------------------")
#        print("Scale =", scale)
        return {'FINISHED'}


class PRESCALE_PG_props(PropertyGroup):

    default_first: bpy.props.FloatProperty(
        default=1
    )
    
    default_second: bpy.props.FloatProperty(
        default=1
    )
    
    l1: bpy.props.FloatProperty(
        name="Get",
        subtype="DISTANCE",
        min=0.001,
        get=get_float1,
        set=set_float1
    )
    
    l2: bpy.props.FloatProperty(
        name="Set",
        subtype="DISTANCE",
        min=0.001,
        get=get_float2,
        set=set_float2
    )
    
    use_x: bpy.props.BoolProperty (
        name=" X", 
        default = True, 
        description="Use local X axis to scale"
    )
        
    use_y: bpy.props.BoolProperty (
        name=" Y", 
        default = True, 
        description="Use local Y axis to scale"
    )
        
    use_z: bpy.props.BoolProperty (
        name=" Z", 
        default = True, 
        description="Use local Z axis to scale"
    )
        
    use_cursor: bpy.props.BoolProperty (
        name="Cursor as origin", 
        default = False, 
        description="Use 3D Cursor as origin to scale"
    )
        
    selection_only: bpy.props.BoolProperty (
        name="Selection only", 
        default = False, 
        description="Use only selected elements to scale"
    )
        
    
class PRESCALE_PT_panel(Panel):
    bl_label = "Precision Scaler"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'PreScale'
   
    def draw(self, context):                       
        scale_props = context.scene.PRESCALE_PG_props
        active_object = context.active_object
        
        layout = self.layout
        col = layout.column(align = True)
        row1 = col.row(align = True) 
        row1.prop(scale_props, "l1", text="")
        row1.scale_x = 0.5
        row1.operator("precision.scaler", icon="TRACKING_FORWARDS", text="Get").action = "GET"
        
        col = layout.column(align = True)
        row2 = col.row(align = True)
        row2.prop(scale_props, "l2", text="")
        row2.scale_x = 0.5
        row2.operator("precision.scaler", icon="TRACKING_BACKWARDS", text="Set").action = "SET"
        
        col = layout.column(align = True)
        row3 = col.row(align = True)
        row3.prop(scale_props, "use_x")
        row3.prop(scale_props, "use_y")
        row3.prop(scale_props, "use_z")        
        
        col = layout.column(align = True)
        sub_row = col.row()
        sub_col1 = sub_row.column()
        sub_sub_row = sub_col1.row() 
        sub_sub_col = sub_sub_row.column()             
#        sub_sub_col.prop(scale_props, "use_cursor", toggle=True)
        sub_sub_col.prop(scale_props, "use_cursor")
        sub_sub_row = sub_col1.row() 
        sub_sub_col = sub_sub_row.column()
        if active_object and active_object.type == 'MESH' and context.mode == 'OBJECT':
            sub_sub_col.enabled = False  
        sub_sub_col.prop(scale_props, "selection_only") 
        
        sub_col2 = sub_row.column()
        sub_col2.scale_x = 0.725  
        sub_col2.scale_y = 2            
        sub_col2.operator("precision.scaler", icon="TRANSFORM_ORIGINS", text="Scale").action = "SCALE"


# Add-ons Preferences Update Panel

# Define Panel classes for updating
panels = (
        PRESCALE_PT_panel,
        )
        
def update_panel(self, context):
    message = "PreScale: Updating Panel locations has failed"
    try:
        for panel in panels:
            if "bl_rna" in panel.__dict__:
                bpy.utils.unregister_class(panel)

        for panel in panels:
            panel.bl_category = context.preferences.addons[__name__].preferences.category
            bpy.utils.register_class(panel)

    except Exception as e:
        print("\n[{}]\n{}\n\nError:\n{}".format(__name__, message, e))
        pass


class PreScalerPreferences(AddonPreferences):
    # this must match the addon name, use '__package__'
    # when defining this in a submodule of a python package.
    bl_idname = __name__

    category: bpy.props.StringProperty(
            #name="Tab Category",
            description="Choose a name for the category of the panel",
            default="PreScale",
            update=update_panel
            )

    def draw(self, context):
        layout = self.layout

#        row = layout.row()
#        col = row.column()
#        col.label(text="Tab Category:")
#        col.prop(self, "category", text="")
        box = layout.box()
        row = box.row(align=True)
        row.label(text='Panel Category (3D View):')
        row.prop(self, 'category', text="")
        

classes = (
    PRESCALE_OT_operator,
    PRESCALE_PG_props,
    PRESCALE_PT_panel,
    PreScalerPreferences,
)

register, unregister = bpy.utils.register_classes_factory(classes)

def register():    
    for c in classes:
        bpy.utils.register_class(c)

    bpy.types.Scene.PRESCALE_PG_props = bpy.props.PointerProperty(type = PRESCALE_PG_props)
    update_panel(None, bpy.context)

def unregister():
    for c in classes:
        bpy.utils.unregister_class(c)
    
    del bpy.types.Scene.PRESCALE_PG_props
    
if __name__ == "__main__":
    register()
