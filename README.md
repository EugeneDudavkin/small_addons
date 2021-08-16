# small_addons
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

## lock_unlock.py
simple addon that adds operator to lock selected and unlock all (Freeze/Unfreeze 3ds Max like).

just add any key in Keymaps for this operator `objects.lock_unlock` and choose action

![lock-unlock](https://user-images.githubusercontent.com/87300864/129525373-90708996-2242-4b6f-8768-c16efef1cd79.png)

## Outliner_Menu_Entries.py
new entries for Outliner context for Objects and for Collections selected:

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

## Switch_Active_Collection_0_1_1.py
Switching to Collection where selected active object located

![SAC_0 1 1](https://user-images.githubusercontent.com/87300864/129539505-6ce278b3-5224-4fbe-8051-9086a7c5eaa4.png)
