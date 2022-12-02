## Active_Camera_menu.py
simple addon that add menu entry when any Camera object is selected.

To make it always accessible in RMB menu, if even nothing is selected, replace code with this

```
def cameras_specials_menu(self, contxt):
    self.layout.separator()
    self.layout.menu(VIEW3D_MT_cameras_main.bl_idname)
```

![Active_Camera_menu](https://user-images.githubusercontent.com/87300864/129523178-0064caf0-fcb9-4e57-96e4-1cba47f61dfd.png)
----------------------------------------------------------------------------------------------------    ----------------------------------------------------------------------------------------------------      

## Collection_Visibility.py
quick switching between objects type visibility in the collection.

Works also from 3d View (if you add keymap for it), BUT
instead of using active collection it uses selected objects and use all their collection where they located.

![Collection_Visibility_1](https://user-images.githubusercontent.com/87300864/129524186-686d3100-978a-4e47-bdbe-94b2920b593d.png)

Also if you want it to be like this

![Collection_Visibility_2](https://user-images.githubusercontent.com/87300864/129524273-9ce53e89-e6ba-440d-bfa6-673f4ef597fc.png)

just rename `OUTLINER_MT_collection_visibility` to `OUTLINER_MT_collection` at the bottom in the script file.
----------------------------------------------------------------------------------------------------    ----------------------------------------------------------------------------------------------------  

## Inactive_Shading_v_1_0_8.py
Makes all unselected (inactive) objects display as wire or bounds, 

with posibility add selected active collection to ignore list as many as you need

![IS_1_0_8](https://user-images.githubusercontent.com/87300864/129542905-4467f689-2404-4832-b70e-6ce52a89ae84.png)
![1_0_8](https://user-images.githubusercontent.com/87300864/129542523-58ae3b39-e62c-462d-9034-4bfe18bd99b2.png)
----------------------------------------------------------------------------------------------------    ----------------------------------------------------------------------------------------------------  

## Lock_unlock.py
simple addon that adds operator to lock selected and unlock all (Freeze/Unfreeze 3ds Max like). 

For those who do not want extra actions in Outliner.

just add any key in Keymaps for this operator `objects.lock_unlock` and choose action

![lock-unlock](https://user-images.githubusercontent.com/87300864/129525373-90708996-2242-4b6f-8768-c16efef1cd79.png)
----------------------------------------------------------------------------------------------------    ----------------------------------------------------------------------------------------------------  

## Outliner_Menu_Entries.py
new entries for Outliner context for Objects and for Collections selected.

![Outliner_Menu_Entries](https://user-images.githubusercontent.com/87300864/129544401-e99efe1a-0288-4dbe-8cd4-f349b28359e0.png)

For objects:
1. Duplicate - for multiple selected objects
2. Duplicate Hierarchy - for multiple selected objects without selecting parented elements
3. Duplicate Instance - for multiple selected objects
4. Duplicate Instance Hierarchy - for multiple selected objects without selecting parented elements
5. Select Hierarchy Multi - for multiple selected objects

For collections (possibile with new ‘selected_ids’ feature):
1. Select Objects - for multiple selected collections
2. Duplicate Collections - for multiple selected collections (thanks for people from blender.stackexchange)
3. Duplicate Linked - for multiple selected collections
----------------------------------------------------------------------------------------------------    ----------------------------------------------------------------------------------------------------  

## Precision_Scaler.py
Simple addon to scale object. Starting length and final length between two points, and then scale to match values.

There is option to change Panel category name in addon preferences.

Update 0.1.1:
* added "Selection only" option - to scale only selected elements in Edit mode.
* added posibility to Get length between two objects in Object mode.
* "Scale" works for multiple selection in Edit or Object mode.

![Precision_Scaler_0 1 1](https://user-images.githubusercontent.com/87300864/130333366-9b955599-4a7e-4cb2-8055-220b53d8c940.png)

https://user-images.githubusercontent.com/87300864/129952496-38d0469b-2a67-441b-be82-a6e0c4805c34.mp4
----------------------------------------------------------------------------------------------------    ----------------------------------------------------------------------------------------------------  

## Select_Shape_Keys_Vertices.py
Simple addon to select vertices affected by shape keys.

![Select_Shape_Keys_Vertices](https://user-images.githubusercontent.com/87300864/205247743-23455fae-fe6f-4e7f-b1db-40a88b223501.jpg)
----------------------------------------------------------------------------------------------------    ----------------------------------------------------------------------------------------------------  

## Switch_Active_Collection_0_1_1.py
Make active Collection where selected active object located

![SAC_0 1 1](https://user-images.githubusercontent.com/87300864/129539505-6ce278b3-5224-4fbe-8051-9086a7c5eaa4.png)

If you don't need icon in Outliner, then just delete or comment lines 72 and 78 
```
bpy.types.OUTLINER_HT_header.append(draw_sync_collection)
```
and 
```
bpy.types.OUTLINER_HT_header.remove(draw_sync_collection)
```
![0 1 1](https://user-images.githubusercontent.com/87300864/135801891-3753804c-5bd3-4b24-b4fd-d8a425233d23.png)
----------------------------------------------------------------------------------------------------    ----------------------------------------------------------------------------------------------------  

## UV_map_list_tools.py
addon with options to moving UV up and down in the list and sorting.

![UV_sorting](https://user-images.githubusercontent.com/87300864/129541363-132d5855-9732-4217-ace9-a156f9ba11f6.png)

also there is Batch tools for UV, 

you can get this addon menus here https://blenderartists.org/t/select-sync-uv-channel-layer-between-multiple-objects/1314529/5

![1_1](https://user-images.githubusercontent.com/87300864/129954345-dfcb9034-fa6b-43da-90a1-254a0f6c749e.png)
![2_2](https://user-images.githubusercontent.com/87300864/129954366-a4a89b6b-1b15-4bf8-b20b-dd52506ed41a.png)
----------------------------------------------------------------------------------------------------    ----------------------------------------------------------------------------------------------------

## switch_collection_by_active_object.py
If it's active, it will switch collection by clicking on object.

![switch_collection_by_active_object](https://user-images.githubusercontent.com/87300864/205039365-7ee8bff6-a85c-4947-9394-50b464c9e989.png)

https://user-images.githubusercontent.com/87300864/205099052-58a57b4d-47fa-4041-ad77-05db81d7d06a.mp4
