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

from bpy.app.handlers import persistent

from bpy.props import (IntProperty,
                       BoolProperty,
                       StringProperty,
                       PointerProperty,
                       CollectionProperty)

from bpy.types import (Menu,
                       Operator,
                       Panel,
                       PropertyGroup,
                       UIList)

bl_info = {
    "name": "Inactive Shading Style",
    "author": "APEC, Christopher Kohl, MACHIN3",
    "version": (1, 0, 8),
    "blender": (2, 82, 0),
    "location": "View3D > Properties",
    "description": "Toggle wire/bounds shading style for inactive meshes.",
    "wiki_url": "https://blenderartists.org/t/shading-for-inactive-objects-in-viewport-wireframe/1206498",
    "tracker_url": "",
    "category": "3D View"
}


oldactive = None
oldsel = None

# -------------------------------------------------------------------
#   Operators
# -------------------------------------------------------------------

class CUSTOM_OT_actions(Operator):
    """Move items up and down, add and remove"""
    bl_idname = "custom.list_action"
    bl_label = "List Actions"
    bl_description = "Move items up and down, add and remove"
    bl_options = {'REGISTER'}

    action: bpy.props.EnumProperty(
        items=(
            ('UP', "Up", ""),
            ('DOWN', "Down", ""),
            ('REMOVE', "Remove", ""),
            ('ADD', "Add", "")))

    def invoke(self, context, event):
        scn = context.scene
        idx = scn.custom_index

        try:
            item = scn.custom[idx]
        except IndexError:
            pass
        else:
            if self.action == 'DOWN' and idx < len(scn.custom) - 1:
                item_next = scn.custom[idx+1].name
                scn.custom.move(idx, idx+1)
                scn.custom_index += 1
                info = 'Item "%s" moved to position %d' % (item.name, scn.custom_index + 1)
                self.report({'INFO'}, info)

            elif self.action == 'UP' and idx >= 1:
                item_prev = scn.custom[idx-1].name
                scn.custom.move(idx, idx-1)
                scn.custom_index -= 1
                info = 'Item "%s" moved to position %d' % (item.name, scn.custom_index + 1)
                self.report({'INFO'}, info)

            elif self.action == 'REMOVE':
                info = 'Item "%s" removed from list' % (scn.custom[idx].name)
                scn.custom_index -= 1
                scn.custom.remove(idx)
                self.report({'INFO'}, info)

        if self.action == 'ADD':
            act_coll = context.view_layer.active_layer_collection.collection
            if act_coll.name in [c[1].name for c in scn.custom.items()]:
                info = '"%s" already in the list' % (act_coll.name)
            else:
                item = scn.custom.add()
                item.coll_ptr = act_coll
                item.name = item.coll_ptr.name
                scn.custom_index = (len(scn.custom)-1)
                info = '%s added to list' % (item.name)

            self.report({'INFO'}, info)
            
#            else:
#                self.report({'INFO'}, "Nothing selected in the Viewport")
        return {"FINISHED"}


class CUSTOM_OT_clearList(Operator):
    """Clear all items of the list"""
    bl_idname = "custom.clear_list"
    bl_label = "Clear List"
    bl_description = "Clear all items of the list"
    bl_options = {'INTERNAL'}

    @classmethod
    def poll(cls, context):
        return bool(context.scene.custom)

    def invoke(self, context, event):
        return context.window_manager.invoke_confirm(self, event)

    def execute(self, context):
        if bool(context.scene.custom):
            context.scene.custom.clear()
            self.report({'INFO'}, "All items removed")
        else:
            self.report({'INFO'}, "Nothing to remove")
        return{'FINISHED'}


# -------------------------------------------------------------------
#   Drawing
# -------------------------------------------------------------------

class CUSTOM_UL_items(UIList):
    def draw_item(self, context, layout, data, item, icon, active_data, active_propname, index):
        split = layout.split(factor=1)
        #split.label(text="Index: %d" % (index))
        split.prop(item.coll_ptr, "name", text="", emboss=False, icon="COLLECTION_NEW")

    def invoke(self, context, event):
        pass   


# -------------------------------------------------------------------
#   Collection
# -------------------------------------------------------------------

class CUSTOM_objectCollection(PropertyGroup):
    #name: StringProperty() -> Instantiated by default
    coll_ptr: PointerProperty(
        name="Collection",
        type=bpy.types.Collection)


# -------------------------------------------------------------------
#   Functions
# -------------------------------------------------------------------
@persistent
def update_shading_style(scene):
    '''
    watch changes in selection or active object
    set display_type accordingly
    '''
    if scene.inactive_wire_shading or scene.inactive_bounds_shading:
        global oldactive, oldsel

        context = bpy.context

        active = context.active_object if context.active_object else None
        sel = context.selected_objects

        if active != oldactive or sel != oldsel:
            oldactive = active
            oldsel = sel

            ignored_objects = get_ignored_collections(context)

            for obj in context.visible_objects:
                if scene.inactive_wire_shading and not scene.inactive_bounds_shading:
                    if obj not in ignored_objects:
                        obj.display_type = 'TEXTURED' if obj in sel else 'WIRE'
                elif scene.inactive_bounds_shading and not scene.inactive_wire_shading:
                    if obj not in ignored_objects:
                        obj.display_type = 'TEXTURED' if obj in sel else 'BOUNDS'


def get_ignored_collections(context):
    #bool_parents = [o for o in context.visible_objects if o.modifiers and any([m for m in o.modifiers if m.type == "BOOLEAN"])]
    #bool_objects = [m.object for o in bool_parents if o is not None for m in o.modifiers if m.type == "BOOLEAN" and m.operand_type == "OBJECT" and m.object is not None]
    #bool_collections = [m.collection for o in bool_parents for m in o.modifiers if m.type == "BOOLEAN" and m.operand_type == "COLLECTION" and m.collection is not None]
    #collection_objects = [o for c in bool_collections if c is not None for o in c.all_objects if o.type == "MESH"]
  
    #return bool_objects + collection_objects + ignored_collection_objects
       
    collection_names = context.scene.custom

    collections = [col for col in bpy.data.collections if col.name in collection_names]
    ignored_collections = [obj for col in collections for obj in col.all_objects if obj.type == "MESH"]
    return  ignored_collections


def PanelInactiveShading(self, context):
    layout = self.layout
    layout.separator()
    
    box = layout.box()
    box.label(text="Inactive Shading")
    split = box.split(factor = 0.5)
    wire = split.column()
    if context.scene.inactive_bounds_shading:
        wire.enabled=False
    wire.prop(context.scene, "inactive_wire_shading", text="Wire")
    bounds = split.column()
    if context.scene.inactive_wire_shading:
        bounds.enabled=False
    bounds.prop(context.scene, "inactive_bounds_shading", text="Bounds")
    
    # Collections List panel - start 
    scn = bpy.context.scene
    
    row = box.row()
    row.prop(scn, "expanded",
        icon="TRIA_DOWN" if scn.expanded else "TRIA_RIGHT",
        icon_only=True, emboss=False
    )
    row.label(text="Ignored Collections")
    if scn.expanded:
        row = box.row()
        rows = 3        
        row.template_list("CUSTOM_UL_items", "", scn, "custom", scn, "custom_index", rows=rows)

        col = row.column(align=True)
        col.operator("custom.list_action", icon='ZOOM_IN', text="").action = 'ADD'
        col.operator("custom.list_action", icon='ZOOM_OUT', text="").action = 'REMOVE'
        col.separator()
        col.operator("custom.list_action", icon='TRIA_UP', text="").action = 'UP'
        col.operator("custom.list_action", icon='TRIA_DOWN', text="").action = 'DOWN'

        #row = layout.row()
        col = box.column(align=True)
        row = col.row(align=True)
        row.operator("custom.clear_list", icon="X")
    # Collection List panel - end
    
# -------------------------------------------------------------------
#   Register & Unregister
# -------------------------------------------------------------------

classes = (
    CUSTOM_OT_actions,   
    CUSTOM_OT_clearList,
    CUSTOM_UL_items,
    CUSTOM_objectCollection,
)

def register():
    from bpy.utils import register_class
    for cls in classes:
        register_class(cls)

    # Custom scene properties
    bpy.types.Scene.custom = CollectionProperty(type=CUSTOM_objectCollection)
    bpy.types.Scene.custom_index = IntProperty()
    
    bpy.types.Scene.expanded = bpy.props.BoolProperty(default=False)
    
    def update_inactive_shading(self, context):
        '''
        reset the display type of all visible objects, when scene.inactive_shading is toggled
        '''

        vis = context.visible_objects
        ignored_objects = get_ignored_collections(context)

        # enabled - set display style according to 1. object being active or among selection: TEXTURED, 2. object not selected: WIRE
        if context.scene.inactive_wire_shading or context.scene.inactive_bounds_shading:
            if context.scene.inactive_wire_shading and context.scene.inactive_bounds_shading:
                context.scene.inactive_wire_shading = False
                context.scene.inactive_bounds_shading = False

            active = context.active_object if context.active_object else None

            sel = [obj for obj in context.selected_objects if obj != active]
            
            for obj in vis:
                if obj not in ignored_objects:
                    if obj in sel or obj == active:
                        if obj.display_type != 'TEXTURED':
                            obj.display_type = 'TEXTURED'

                    else:
                        if context.scene.inactive_wire_shading and not context.scene.inactive_bounds_shading:
                            if obj.display_type != 'WIRE':
                                obj.display_type = 'WIRE'
                        elif context.scene.inactive_bounds_shading and not context.scene.inactive_wire_shading:
                            if obj.display_type != 'BOUNDS':
                                obj.display_type = 'BOUNDS'

        # disabled - set all visible objects to TEXTURED
        else:
            for obj in vis:
                if obj not in ignored_objects and obj.display_type != 'TEXTURED':
                    obj.display_type = 'TEXTURED'

    # You can set one of these to True by default if you prefer. Do NOT set both to True.
    bpy.types.Scene.inactive_wire_shading = bpy.props.BoolProperty(name="Inactive Wire Shading", default=False, update=update_inactive_shading)
    bpy.types.Scene.inactive_bounds_shading = bpy.props.BoolProperty(name="Inactive Bounds Shading", default=False, update=update_inactive_shading)

    bpy.types.VIEW3D_PT_shading_color.append(PanelInactiveShading)

    bpy.app.handlers.depsgraph_update_post.append(update_shading_style)
    bpy.app.handlers.undo_post.append(update_shading_style)
    bpy.app.handlers.redo_post.append(update_shading_style)


def unregister():
    from bpy.utils import unregister_class
    for cls in reversed(classes):
        unregister_class(cls)

#    del bpy.types.Scene.custom
#    del bpy.types.Scene.custom_index
#    
#    '''
#    after disabling addon, make all objects TEXTURED
#    '''
#    context = bpy.context
#    sel = context.selected_objects

#    ignored_objects = get_ignored_collections(context)

#    for obj in context.visible_objects:
#        if obj not in ignored_objects and obj.display_type != 'TEXTURED':
#            obj.display_type = 'TEXTURED'
       
    bpy.app.handlers.depsgraph_update_post.remove(update_shading_style)
    bpy.app.handlers.undo_post.remove(update_shading_style)
    bpy.app.handlers.redo_post.remove(update_shading_style)

    bpy.types.VIEW3D_PT_shading_color.remove(PanelInactiveShading)
    
    del bpy.types.Scene.expanded

    del bpy.types.Scene.inactive_wire_shading
    del bpy.types.Scene.inactive_bounds_shading
    
if __name__ == "__main__":
    register()