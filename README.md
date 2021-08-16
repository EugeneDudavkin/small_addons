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

