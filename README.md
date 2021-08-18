## Active_Camera_menu.py
simple addon that add menu entry when any Camera object is selected.

To make it always accessible in RMB menu, if even nothing is selected, replace code with this

```
def cameras_specials_menu(self, contxt):
    self.layout.separator()
    self.layout.menu(VIEW3D_MT_cameras_main.bl_idname)
```

![Active_Camera_menu](https://user-images.githubusercontent.com/87300864/129523178-0064caf0-fcb9-4e57-96e4-1cba47f61dfd.png)

## Collection_Visibility.py
quick switching between objects type visibility in the collection.

Works also from 3d View (if you add keymap for it), BUT
instead of using active collection it uses selected objects and use all their collection where they located.

![Collection_Visibility_1](https://user-images.githubusercontent.com/87300864/129524186-686d3100-978a-4e47-bdbe-94b2920b593d.png)

Also if you want it to be like this

![Collection_Visibility_2](https://user-images.githubusercontent.com/87300864/129524273-9ce53e89-e6ba-440d-bfa6-673f4ef597fc.png)

just rename `OUTLINER_MT_collection_visibility` to `OUTLINER_MT_collection` at the bottom in the script file.

## Inactive_Shading_v_1_0_8.py
Makes all unselected (inactive) objects display as wire or bounds, 

with posibility add selected active collection to ignore list as many as you need

![IS_1_0_8](https://user-images.githubusercontent.com/87300864/129542905-4467f689-2404-4832-b70e-6ce52a89ae84.png)
![1_0_8](https://user-images.githubusercontent.com/87300864/129542523-58ae3b39-e62c-462d-9034-4bfe18bd99b2.png)

## Lock_unlock.py
simple addon that adds operator to lock selected and unlock all (Freeze/Unfreeze 3ds Max like). 

For those who do not want extra actions in Outliner.

just add any key in Keymaps for this operator `objects.lock_unlock` and choose action

![lock-unlock](https://user-images.githubusercontent.com/87300864/129525373-90708996-2242-4b6f-8768-c16efef1cd79.png)

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

## Precision_Scaler.py
Simple addon to scale object. Starting length and final length between two points, and then scale to match values.

![Precision_Scaler_0 0 1](https://user-images.githubusercontent.com/87300864/129952512-b86d7f00-0aae-459f-85e8-caa26c42b98e.png)

https://user-images.githubusercontent.com/87300864/129952496-38d0469b-2a67-441b-be82-a6e0c4805c34.mp4

## Switch_Active_Collection_0_1_1.py
Make active Collection where selected active object located

![SAC_0 1 1](https://user-images.githubusercontent.com/87300864/129539505-6ce278b3-5224-4fbe-8051-9086a7c5eaa4.png)

## UV_map_list_tools.py
addon with options to moving UV up and down in the list and sorting.

![UV_sorting](https://user-images.githubusercontent.com/87300864/129541363-132d5855-9732-4217-ace9-a156f9ba11f6.png)

also there is Batch tools for UV, 

you can get this addon menus here https://blenderartists.org/t/select-sync-uv-channel-layer-between-multiple-objects/1314529/5

![1](https://user-images.githubusercontent.com/87300864/129541521-0ae5a313-b1b5-4b2e-9802-4602cc75f77a.png)
![2](https://user-images.githubusercontent.com/87300864/129541527-448cf1ac-17fc-4409-8f90-21400f7c79d9.png)
