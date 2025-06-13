import bpy
import math
from bpy.props import (
    StringProperty, FloatProperty, IntProperty,
    CollectionProperty, EnumProperty, PointerProperty, IntProperty
)
from bpy.types import Panel, Operator, PropertyGroup

class FXImageSlot(PropertyGroup):
    image_path: StringProperty(name="Image", subtype='FILE_PATH')
    size: FloatProperty(name="Size", default=1.0, min=0.01)
    count: IntProperty(name="Count", default=8, min=1)

class FXSettings(PropertyGroup):
    items: CollectionProperty(type=FXImageSlot)
    effect_type: EnumProperty(
        name="Effect Type",
        items=[
            ('CIRCLE', "Circle", ""),
            ('SPIRAL', "Spiral", "")
        ],
        default='CIRCLE'
    )
    spiral_height: FloatProperty(name="Spiral Height", default=5.0, min=0.1)

class FX_PT_MainPanel(Panel):
    bl_label = "Ring FX Generator"
    bl_idname = "FX_PT_main_panel"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'Particle Tools'

    def draw(self, context):
        layout = self.layout
        fx = context.scene.fx_settings

        layout.prop(fx, "effect_type")
        if fx.effect_type == 'SPIRAL':
            layout.prop(fx, "spiral_height")

        col = layout.column()
        col.operator("fx.add_slot", text="＋ Add Image Slot")
        for i, item in enumerate(fx.items):
            box = col.box()
            row = box.row()

            button_col = row.column(align=True)
            button_col.operator("fx.move_slot_up", text="↑").index = i
            button_col.operator("fx.move_slot_down", text="↓").index = i
            button_col.operator("fx.add_slot", text="＋")
            button_col.operator("fx.remove_slot", text="ー").index = i

            content_col = row.column()
            content_col.prop(item, "image_path")
            content_col.prop(item, "size")
            content_col.prop(item, "count")

        layout.operator("fx.generate_effect", text="✨ Generate")

class FX_OT_AddSlot(Operator):
    bl_idname = "fx.add_slot"
    bl_label = "Add Image Slot"

    def execute(self, context):
        context.scene.fx_settings.items.add()
        return {'FINISHED'}

class FX_OT_RemoveSlot(Operator):
    bl_idname = "fx.remove_slot"
    bl_label = "Remove Image Slot"

    index: IntProperty()

    def execute(self, context):
        fx = context.scene.fx_settings
        if 0 <= self.index < len(fx.items):
            fx.items.remove(self.index)
        return {'FINISHED'}

class FX_OT_MoveSlotUp(Operator):
    bl_idname = "fx.move_slot_up"
    bl_label = "Move Slot Up"

    index: IntProperty()

    def execute(self, context):
        fx = context.scene.fx_settings
        if self.index > 0:
            fx.items.move(self.index, self.index - 1)
        return {'FINISHED'}

class FX_OT_MoveSlotDown(Operator):
    bl_idname = "fx.move_slot_down"
    bl_label = "Move Slot Down"

    index: IntProperty()

    def execute(self, context):
        fx = context.scene.fx_settings
        if self.index < len(fx.items) - 1:
            fx.items.move(self.index, self.index + 1)
        return {'FINISHED'}

class FX_OT_GenerateEffect(Operator):
    bl_idname = "fx.generate_effect"
    bl_label = "Generate FX"

    def execute(self, context):
        fx = context.scene.fx_settings
        slots = [slot for slot in fx.items if slot.image_path]
        if not slots:
            self.report({'WARNING'}, "No valid image slots found.")
            return {'CANCELLED'}

        spiral = fx.effect_type == 'SPIRAL'

        for slot_index, slot in enumerate(slots):
            total = slot.count
            for i in range(total):
                global_index = sum(s.count for s in slots[:slot_index]) + i
                total_instances = sum(s.count for s in slots)
                angle = (global_index / total_instances) * 2 * math.pi

                if spiral:
                    x = math.cos(angle) * 3
                    y = math.sin(angle) * 3
                    z = (i / slot.count) * fx.spiral_height
                else:
                    x = math.cos(angle) * 3
                    y = math.sin(angle) * 3
                    z = 1

                bpy.ops.mesh.primitive_plane_add(size=slot.size, location=(x, y, z))
                plane = context.active_object
                plane.rotation_mode = 'XYZ'
                plane.rotation_euler[2] = 0
                plane.rotation_euler[0] = math.radians(90)
                plane.rotation_euler[1] = 0

                # Track to empty at center to always face front
                bpy.ops.object.empty_add(type='PLAIN_AXES', location=(0, 0, 0))
                tracker = bpy.context.active_object
                plane.select_set(True)
                bpy.context.view_layer.objects.active = plane
                constraint = plane.constraints.new(type='TRACK_TO')
                constraint.target = tracker
                constraint.track_axis = 'TRACK_Z'
                constraint.up_axis = 'UP_Y'  # 正面から見て立てる

                mat = self.create_image_material(slot.image_path)
                if mat:
                    plane.data.materials.append(mat)

                # 回転アニメーションを追加
                plane.animation_data_create()
                plane.animation_data.action = bpy.data.actions.new(name="FXRotation")
                fcurves = plane.animation_data.action.fcurves.new(data_path="rotation_euler", index=2)
                fcurves.keyframe_points.add(2)
                fcurves.keyframe_points[0].co = 0, 0
                fcurves.keyframe_points[1].co = 60, math.radians(360)

        return {'FINISHED'}

    def create_image_material(self, image_path):
        img = bpy.data.images.load(image_path, check_existing=True)
        mat = bpy.data.materials.new(name="FXMaterial")
        mat.use_nodes = True
        nodes = mat.node_tree.nodes
        links = mat.node_tree.links

        nodes.clear()
        output = nodes.new(type='ShaderNodeOutputMaterial')
        shader = nodes.new(type='ShaderNodeBsdfTransparent')
        tex = nodes.new(type='ShaderNodeTexImage')
        mix = nodes.new(type='ShaderNodeMixShader')
        bsdf = nodes.new(type='ShaderNodeBsdfDiffuse')

        tex.image = img
        tex.extension = 'CLIP'

        links.new(tex.outputs["Alpha"], mix.inputs[0])
        links.new(shader.outputs[0], mix.inputs[1])
        links.new(bsdf.outputs[0], mix.inputs[2])
        links.new(mix.outputs[0], output.inputs[0])
        links.new(tex.outputs['Color'], bsdf.inputs['Color'])

        mat.blend_method = 'BLEND'
        return mat

classes = [
    FXImageSlot, FXSettings,
    FX_PT_MainPanel,
    FX_OT_AddSlot, FX_OT_RemoveSlot,
    FX_OT_MoveSlotUp, FX_OT_MoveSlotDown,
    FX_OT_GenerateEffect
]

def register():
    for cls in classes:
        bpy.utils.register_class(cls)
    bpy.types.Scene.fx_settings = PointerProperty(type=FXSettings)

def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)
    del bpy.types.Scene.fx_settings

if __name__ == "__main__":
    register()
