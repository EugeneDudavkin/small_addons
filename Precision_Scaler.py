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
    "version": (0, 0, 1),
    "blender": (2, 93, 0),
    "location": "View3d > N-Panel > PreScaler",
    "description": "Scale selected by defined length", 
    "doc_url": "",
    "tracker_url": "",      
    "category": "3D View"
}

import bpy
import bmesh
from bpy.types import Operator, PropertyGroup, Panel

def get_float1(self):
    return self["l1"]

def set_float1(self, value):
    self["l1"] = value

def get_float2(self):
    return self["l2"]

def set_float2(self, value):
    self["l2"] = value

def distance_between():
    obj = bpy.context.edit_object
    me = obj.data
    bm = bmesh.from_edit_mesh(me)

    elem_list1 = []

    for g in bm.select_history:
        elem_list1.append(g)
            
    point_first  = elem_list1[0].co
    point_second = elem_list1[1].co

    distance = (point_second - point_first).length    
    return distance


class PRESCALE_OT_operator(Operator):
    bl_idname = "precision.scaler"
    bl_label = "Precision Scaler"
    #bl_description = "Scale by defined length"

    action: bpy.props.EnumProperty (
        items=[('GET','GET',''),
               ('SET','SET',''),
               ('SCALE','SCALE','')])
               
    def execute(self, context):
        scale_props = context.scene.PRESCALE_PG_props       
    
        if self.action == "GET":            
            try:
                scale_props.l1 = distance_between() 
            except:
                self.report({'WARNING'}, 'Need to click on first and second vertices')
                return {'CANCELLED'}           
        
        if self.action == "SET":
            try:
                scale_props.l2 = distance_between()
            except:
                self.report({'WARNING'}, 'Need to click on first and second vertices')
                return {'CANCELLED'}
        
        if self.action == "SCALE":                    
            real_cursor = bpy.context.scene.cursor.matrix
            real_transform = bpy.context.scene.transform_orientation_slots[0].type 
            
            bpy.context.scene.cursor.matrix = bpy.context.object.matrix_world
            obj_origin = bpy.context.scene.cursor.matrix
              
            bpy.ops.object.mode_set(mode='OBJECT')            
            
            if scale_props.use_cursor == True:
                bpy.context.scene.cursor.matrix = real_cursor
                bpy.context.scene.transform_orientation_slots[0].type = 'CURSOR' 
                bpy.context.scene.tool_settings.use_transform_data_origin = True
                bpy.ops.object.origin_set(type='ORIGIN_CURSOR', center='MEDIAN')                
                bpy.ops.transform.transform(mode='ALIGN', orient_type='CURSOR')
                bpy.context.scene.tool_settings.use_transform_data_origin = False               
            
            scale = scale_props.l2 / scale_props.l1        
            
            if scale_props.use_x == True:
                bpy.context.object.scale[0] = scale
            
            if scale_props.use_x == False:
                bpy.context.object.scale[0] = 1
            
            if scale_props.use_y == True:
                bpy.context.object.scale[1] = scale
            
            if scale_props.use_y == False:
                bpy.context.object.scale[1] = 1
            
            if scale_props.use_z == True:
                bpy.context.object.scale[2] = scale
            
            if scale_props.use_z == False:
                bpy.context.object.scale[2] = 1
                
            bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
            bpy.context.scene.transform_orientation_slots[0].type = real_transform
            bpy.context.scene.cursor.matrix = obj_origin
            bpy.context.scene.tool_settings.use_transform_data_origin = True
            bpy.ops.object.origin_set(type='ORIGIN_CURSOR', center='MEDIAN')            
            bpy.ops.transform.transform(mode='ALIGN', orient_type='CURSOR')
            bpy.context.scene.tool_settings.use_transform_data_origin = False
            
            bpy.context.scene.cursor.matrix = real_cursor

            bpy.ops.object.mode_set(mode='EDIT')

        #print("----------------------")
        #print("Scale =", scale)
        return {'FINISHED'}


class PRESCALE_PG_props(PropertyGroup):

    l1: bpy.props.FloatProperty(
        name="Get",
        subtype="DISTANCE",
        get=get_float1,
        set=set_float1,
        min=0.001,
        default=1
    )
    
    l2: bpy.props.FloatProperty(
        name="Set",
        subtype="DISTANCE",
        get=get_float2,
        set=set_float2,
        min=0.001,
        default=1
    )
    
    use_x: bpy.props.BoolProperty (
        name=" X", 
        default = True, 
        description="Use local X axis to scale")
        
    use_y: bpy.props.BoolProperty (
        name=" Y", 
        default = True, 
        description="Use local Y axis to scale")
        
    use_z: bpy.props.BoolProperty (
        name=" Z", 
        default = True, 
        description="Use local Z axis to scale")
        
    use_cursor: bpy.props.BoolProperty (
        name="Cursor as origin", 
        default = False, 
        description="Use 3D Cursor as origin to scale")
        
    
class PRESCALE_PT_panel(Panel):
    bl_label = "Precision Scaler"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'PreScale'
    
    def draw(self, context):               
        scale_props = context.scene.PRESCALE_PG_props
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
        row4 = col.row(align = True)        
        row4.prop(scale_props, "use_cursor") 
        row4.scale_x = 0.5  
        row4.scale_y = 1.3            
        row4.operator("precision.scaler", icon="TRANSFORM_ORIGINS", text="Scale").action = "SCALE"


classes = (
    PRESCALE_OT_operator,
    PRESCALE_PG_props,
    PRESCALE_PT_panel,
)

register, unregister = bpy.utils.register_classes_factory(classes)

def register():    
    for c in classes:
        bpy.utils.register_class(c)

    bpy.types.Scene.PRESCALE_PG_props = bpy.props.PointerProperty(type = PRESCALE_PG_props)

def unregister():
    for c in classes:
        bpy.utils.unregister_class(c)
    
    del bpy.types.Scene.PRESCALE_PG_props
    
if __name__ == "__main__":
    register()   
