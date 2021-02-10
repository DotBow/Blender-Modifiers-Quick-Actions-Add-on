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

# <pep8 compliant>

import bpy
from bpy.types import AddonPreferences, Operator
from bpy.utils import register_class, unregister_class

from .modules.keymap_manager import (draw_key, register_keymap,
                                     unregister_keymap)

bl_info = {
    "name": "Modfiers Quick Actions",
    "author": "Oleg Stepanov (DotBow)",
    "description": "Perform actions on modifiers under cursor (Apply, Duplicate, Delete)",
    "blender": (2, 90, 0),
    "version": (1, 0, 0),
    "location": "Properties Editor > Modifiers",
    "warning": "",
    "category": "Modifiers"
}


class AddonPreferences(AddonPreferences):
    bl_idname = __name__

    def draw(self, context):
        # Draw keymap
        keys = [('Property Editor', 'object.apply_modifier', None),
                ('Property Editor', 'object.duplicate_modifier', None),
                ('Property Editor', 'object.remove_modifier', None)]
        draw_key(self.layout, keys)


class MQA_OT_ApplyModifier(Operator):
    """Apply modifier under cursor and remove from the stack"""
    bl_idname = "object.apply_modifier"
    bl_label = "Apply Modifier Under Cursor"
    bl_options = {'UNDO', 'INTERNAL'}

    @classmethod
    def poll(cls, context):
        return (bpy.ops.object.modifier_set_active.poll()) and \
            (len(context.active_object.modifiers) > 0)

    def execute(self, context):
        ob = context.active_object
        mod_old = ob.modifiers.active.name
        bpy.ops.object.modifier_set_active('INVOKE_DEFAULT')
        mod_new = ob.modifiers.active.name

        try:
            bpy.ops.object.modifier_apply(modifier=mod_new)
        except RuntimeError as e:
            bpy.ops.object.modifier_set_active(modifier=mod_old)
            return {'FINISHED'}

        if mod_old != mod_new:
            bpy.ops.object.modifier_set_active(modifier=mod_old)

        return {'FINISHED'}


class MQA_OT_DuplicateModifier(Operator):
    """Duplicate modifier under cursor at the same postion at the stack"""
    bl_idname = "object.duplicate_modifier"
    bl_label = "Duplicate Modifier Under Cursor"
    bl_options = {'UNDO', 'INTERNAL'}

    @classmethod
    def poll(cls, context):
        return (bpy.ops.object.modifier_set_active.poll()) and \
            (len(context.active_object.modifiers) > 0)

    def execute(self, context):
        ob = context.active_object
        mod_old = ob.modifiers.active.name
        bpy.ops.object.modifier_set_active('INVOKE_DEFAULT')
        mod_new = ob.modifiers.active.name
        bpy.ops.object.modifier_copy(modifier=mod_new)

        if mod_old != mod_new:
            bpy.ops.object.modifier_set_active(modifier=mod_old)

        return {'FINISHED'}


class MQA_OT_RemoveModifier(Operator):
    """Remove a modifier under cursor from the active object"""
    bl_idname = "object.remove_modifier"
    bl_label = "Remove Modifier Under Cursor"
    bl_options = {'UNDO', 'INTERNAL'}

    @classmethod
    def poll(cls, context):
        return (bpy.ops.object.modifier_set_active.poll()) and \
            (len(context.active_object.modifiers) > 0)

    def execute(self, context):
        ob = context.active_object
        mod_old = ob.modifiers.active.name
        bpy.ops.object.modifier_set_active('INVOKE_DEFAULT')
        mod_new = ob.modifiers.active.name
        bpy.ops.object.modifier_remove(modifier=mod_new)

        if mod_old != mod_new:
            bpy.ops.object.modifier_set_active(modifier=mod_old)

        return {'FINISHED'}


classes = (
    AddonPreferences,
    MQA_OT_ApplyModifier,
    MQA_OT_DuplicateModifier,
    MQA_OT_RemoveModifier
)


def register():
    for cls in classes:
        register_class(cls)

    register_keymap()


def unregister():
    for cls in classes:
        unregister_class(cls)

    unregister_keymap()


if __name__ == "__main__":
    register()
