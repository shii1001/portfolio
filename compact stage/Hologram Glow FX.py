import bpy
import math
from bpy.props import FloatVectorProperty

# -------------------
# 1. シーン初期化
# -------------------
def clear_scene():
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.delete(use_global=False)

# -------------------
# 2. リング（2×3ブロック）生成
# -------------------
def create_ring(radius=2.0, height=0.1, thickness=0.05, segments=32, location=(0, 0, 0)):
    created_objects = []
    angle_step = 2 * math.pi / segments

    for i in range(segments):
        angle = i * angle_step
        base_x = math.cos(angle) * radius
        base_y = math.sin(angle) * radius

        # 2列×3段
        for col in [-0.08, 0.08]:  # 横方向（2列）
            for row in [-0.12, 0.0, 0.12]:  # 縦方向（3段）
                # 正接方向にずらす（角度+π/2）
                offset_angle = angle + math.pi / 2
                x = base_x + col * math.cos(offset_angle)
                y = base_y + col * math.sin(offset_angle)
                z = location[2] + row

                bpy.ops.mesh.primitive_cube_add(size=1, location=(x, y, z))
                cube = bpy.context.object
                cube.scale = (thickness, 0.05, height)
                cube.rotation_euler[2] = angle
                created_objects.append(cube)

    return created_objects

# -------------------
# 3. 発光マテリアル
# -------------------
def add_glow_material(color):
    mat = bpy.data.materials.get("GlowMaterial")
    if not mat:
        mat = bpy.data.materials.new(name="GlowMaterial")
    mat.use_nodes = True
    nodes = mat.node_tree.nodes
    links = mat.node_tree.links

    for node in nodes:
        nodes.remove(node)

    output = nodes.new(type='ShaderNodeOutputMaterial')
    emission = nodes.new(type='ShaderNodeEmission')
    emission.inputs['Color'].default_value = (*color, 1.0)
    emission.inputs['Strength'].default_value = 10.0
    links.new(emission.outputs['Emission'], output.inputs['Surface'])

    return mat

# -------------------
# 4. 回転アニメーション（倍遅く＝240フレーム）
# -------------------
def add_rotation_animation(obj, duration=240):
    obj.rotation_euler = (0, 0, 0)
    obj.keyframe_insert(data_path="rotation_euler", frame=1)
    obj.rotation_euler[2] = 2 * math.pi
    obj.keyframe_insert(data_path="rotation_euler", frame=duration)

    for fc in obj.animation_data.action.fcurves:
        for kp in fc.keyframe_points:
            kp.interpolation = 'LINEAR'

# -------------------
# 5. 生成実行
# -------------------
def generate_hologram(color):
    # clear_scene() # Commented out or removed
    ring_objects = create_ring()
    mat = add_glow_material(color)

    for obj in ring_objects:
        obj.data.materials.append(mat)

    bpy.ops.object.empty_add(type='PLAIN_AXES', location=(0, 0, 0))
    empty = bpy.context.object
    for obj in ring_objects:
        obj.parent = empty
    add_rotation_animation(empty)

# -------------------
# 6. UI定義
# -------------------
class GenerateHologramOperator(bpy.types.Operator):
    bl_idname = "object.generate_hologram"
    bl_label = "Generate Hologram"

    def execute(self, context):
        generate_hologram(context.scene.hologram_color)
        return {'FINISHED'}

class HologramToolPanel(bpy.types.Panel):
    bl_label = "Hologram Tool"
    bl_idname = "VIEW3D_PT_hologram_tool"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'Stage FX'

    def draw(self, context):
        layout = self.layout
        layout.prop(context.scene, "hologram_color", text="Glow Color")
        layout.operator("object.generate_hologram", text="Generate Hologram")

# -------------------
# 7. 登録・解除
# -------------------
def register():
    bpy.utils.register_class(GenerateHologramOperator)
    bpy.utils.register_class(HologramToolPanel)
    bpy.types.Scene.hologram_color = FloatVectorProperty(
        name="Glow Color",
        subtype='COLOR',
        default=(1.0, 0.2, 1.0),
        min=0.0, max=1.0,
        description="Color of the glow"
    )

def unregister():
    bpy.utils.unregister_class(GenerateHologramOperator)
    bpy.utils.unregister_class(HologramToolPanel)
    del bpy.types.Scene.hologram_color

if __name__ == "__main__":
    register()
