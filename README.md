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
quick switching between objects type visibility in the collection

![Collection_Visibility_1](https://user-images.githubusercontent.com/87300864/129524186-686d3100-978a-4e47-bdbe-94b2920b593d.png)

Also if you want it to be like this

![Collection_Visibility_2](https://user-images.githubusercontent.com/87300864/129524273-9ce53e89-e6ba-440d-bfa6-673f4ef597fc.png)

just rename `OUTLINER_MT_collection_visibility` to `OUTLINER_MT_collection` at the bottom in the script file.

