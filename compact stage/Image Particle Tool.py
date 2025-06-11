bl_info = {
    "name": "Multi Petal Generator",
    "blender": (4, 3, 0),
    "category": "ImgFX",
}

import bpy
import os
import math
import random
from bpy.props import (
    StringProperty,
    FloatProperty,
    IntProperty,
    CollectionProperty,
    PointerProperty,
)

from bpy.types import PropertyGroup, UIList, Operator, Panel

# ------------------------------
# 花びら1セットの情報
# ------------------------------
class PetalSet(PropertyGroup):
    image_path: StringProperty(
        name="Image Path",
        subtype='FILE_PATH',
    )
    size: FloatProperty(
        name="Size",
        default=0.5,
        min=0.01,
        max=10.0
    )
    count: IntProperty(
        name="Count",
        default=30,
        min=1,
        max=1000
    )

# ------------------------------
# UIリストの描画
# ------------------------------
class PETAL_UL_petalset_list(UIList):
    def draw_item(self, context, layout, data, item, icon, active_data, active_propname, index):
        box = layout.box()
        box.prop(item, "image_path", text="Image")
        box.prop(item, "size")
        box.prop(item, "count")

# ------------------------------
# ＋ボタン：花びらセットを追加
# ------------------------------
class PETAL_OT_add_petalset(Operator):
    bl_idname = "petal.add_petalset"
    bl_label = "Add Petal Set"

    def execute(self, context):
        context.scene.petal_sets.add()
        context.scene.petal_sets_index = len(context.scene.petal_sets) - 1
        return {'FINISHED'}

# ------------------------------
# −ボタン：花びらセットを削除
# ------------------------------
class PETAL_OT_remove_petalset(Operator):
    bl_idname = "petal.remove_petalset"
    bl_label = "Remove Petal Set"

    def execute(self, context):
        index = context.scene.petal_sets_index
        if index >= 0 and index < len(context.scene.petal_sets):
            context.scene.petal_sets.remove(index)
            context.scene.petal_sets_index = max(0, index - 1)
        return {'FINISHED'}

# ------------------------------
# 花びらの生成処理
# ------------------------------
class PETAL_OT_generate_petals(Operator):
    bl_idname = "petal.generate_petals"
    bl_label = "Generate Petals"

    def execute(self, context):
        collection_name = "ImgEffectCollection"
        if collection_name not in bpy.data.collections:
            col = bpy.data.collections.new(collection_name)
            bpy.context.scene.collection.children.link(col)
        else:
            col = bpy.data.collections[collection_name]

        for i, petalset in enumerate(context.scene.petal_sets):
            image_path = bpy.path.abspath(petalset.image_path)
            if not os.path.exists(image_path):
                self.report({'ERROR'}, f"Image not found: {image_path}")
                continue

            # イメージ読み込み（再読み込み）
            img = None
            for image in bpy.data.images:
                if image.filepath == image_path:
                    img = image
                    img.reload()
                    break
            if not img:
                img = bpy.data.images.load(image_path)

            # マテリアル生成
            mat_name = f"PetalMaterial_{i}"
            mat = bpy.data.materials.get(mat_name)
            if not mat:
                mat = bpy.data.materials.new(name=mat_name)
                mat.use_nodes = True
                bsdf = mat.node_tree.nodes.get("Principled BSDF")
                tex_image = mat.node_tree.nodes.new('ShaderNodeTexImage')
                tex_image.image = img
                mat.node_tree.links.new(tex_image.outputs['Color'], bsdf.inputs['Base Color'])
                mat.node_tree.links.new(tex_image.outputs['Alpha'], bsdf.inputs['Alpha'])
                mat.blend_method = 'BLEND'
                mat.use_backface_culling = False

            # 花びら生成
            for j in range(petalset.count):
                angle = (2 * math.pi) * (j / petalset.count)
                r = 4 * (0.6 + 0.4 * random.random())
                x = r * math.cos(angle)
                y = r * math.sin(angle)
                z = 0.01

                bpy.ops.mesh.primitive_plane_add(size=petalset.size, location=(x, y, z))
                obj = bpy.context.object
                obj.name = f"Petal_{i}_{j}"
                obj.rotation_euler[2] = random.uniform(0, 3.14)
                obj.data.materials.append(mat)

                col.objects.link(obj)
                try:
                    bpy.context.scene.collection.objects.unlink(obj)
                except:
                    pass

        self.report({'INFO'}, "花びらを生成しました")
        return {'FINISHED'}

# ------------------------------
# UIパネル定義
# ------------------------------
class PETAL_PT_panel(Panel):
    bl_label = "Img particle"
    bl_idname = "PETAL_PT_panel"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'Particle Tools'

    def draw(self, context):
        layout = self.layout
        row = layout.row()
        row.template_list("PETAL_UL_petalset_list", "", context.scene, "petal_sets", context.scene, "petal_sets_index")

        col = row.column(align=True)
        col.operator("petal.add_petalset", icon='ADD', text="")
        col.operator("petal.remove_petalset", icon='REMOVE', text="")

        layout.operator("petal.generate_petals", icon="PARTICLES")

# ------------------------------
# 登録 / 解除
# ------------------------------
classes = [
    PetalSet,
    PETAL_UL_petalset_list,
    PETAL_OT_add_petalset,
    PETAL_OT_remove_petalset,
    PETAL_OT_generate_petals,
    PETAL_PT_panel,
]

def register():
    for cls in classes:
        bpy.utils.register_class(cls)
    bpy.types.Scene.petal_sets = CollectionProperty(type=PetalSet)
    bpy.types.Scene.petal_sets_index = IntProperty(default=0)

def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)
    del bpy.types.Scene.petal_sets
    del bpy.types.Scene.petal_sets_index

if __name__ == "__main__":
    register()
