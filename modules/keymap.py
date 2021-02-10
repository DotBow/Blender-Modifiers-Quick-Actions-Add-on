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


def keymap():
    keymap = []

    wm = bpy.context.window_manager
    kc = wm.keyconfigs.addon

    km = kc.keymaps.new(name='Property Editor', space_type='PROPERTIES')

    kmi = km.keymap_items.new(
        "object.apply_modifier", "A", "PRESS", ctrl=True)
    kmi = km.keymap_items.new(
        "object.duplicate_modifier", "D", "PRESS", shift=True)
    kmi = km.keymap_items.new(
        "object.remove_modifier", "X", "PRESS")

    keymap.append((km, kmi))

    return keymap
