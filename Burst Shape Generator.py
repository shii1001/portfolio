import bpy
import random
import math
from bpy.props import EnumProperty, FloatVectorProperty

def clear_scene():
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.delete(use_global=False)

def create_falling_sphere():
    bpy.ops.mesh.primitive_uv_sphere_add(radius=0.4, location=(0, 0, 5))
    sphere = bpy.context.object
    sphere.name = "FallingSphere"
    sphere.location = (0, 0, 5)
    sphere.keyframe_insert(data_path="location", frame=0)
    sphere.location = (0, 0, 0)
    sphere.keyframe_insert(data_path="location", frame=15)

def create_star():
    bpy.ops.mesh.primitive_circle_add(vertices=5, radius=0.15, fill_type='NGON')
    obj = bpy.context.object
    bpy.ops.object.editmode_toggle()
    bpy.ops.mesh.extrude_region_move(TRANSFORM_OT_translate={"value": (0, 0, 0.05)})
    bpy.ops.object.editmode_toggle()
    return obj

def create_heart():
    import bmesh

    mesh = bpy.data.meshes.new("HeartMesh")
    obj = bpy.data.objects.new("Heart", mesh)
    bpy.context.collection.objects.link(obj)
    bpy.context.view_layer.objects.active = obj

    bm = bmesh.new()

    points = [
        (-0.5, 0, 0), (-0.75, 0, 0.3), (-0.5, 0, 0.6),
        (-0.25, 0, 0.6), (0, 0, 0.3),
        (0.25, 0, 0.6), (0.5, 0, 0.6), (0.75, 0, 0.3),
        (0.5, 0, 0), (0, 0, -0.7),
    ]

    verts = [bm.verts.new(p) for p in points]
    bm.faces.new(verts)

    bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
    bmesh.ops.solidify(bm, geom=bm.faces[:] + bm.edges[:] + bm.verts[:], thickness=0.2)

    bm.to_mesh(mesh)
    bm.free()

    return obj

def create_diamond():
    import bmesh

    mesh = bpy.data.meshes.new("DiamondMesh")
    obj = bpy.data.objects.new("Diamond", mesh)
    bpy.context.collection.objects.link(obj)
    bpy.context.view_layer.objects.active = obj

    bm = bmesh.new()

    top_center = bm.verts.new((0, 0, 0.4))
    bottom = bm.verts.new((0, 0, -0.6))

    ring_top = []
    ring_bottom = []
    steps = 8
    radius_top = 0.25
    radius_bottom = 0.5

    for i in range(steps):
        angle = (2 * math.pi / steps) * i
        x_top = math.cos(angle) * radius_top
        y_top = math.sin(angle) * radius_top
        z_top = 0.2
        v_top = bm.verts.new((x_top, y_top, z_top))
        ring_top.append(v_top)

        x_bot = math.cos(angle) * radius_bottom
        y_bot = math.sin(angle) * radius_bottom
        z_bot = 0.0
        v_bot = bm.verts.new((x_bot, y_bot, z_bot))
        ring_bottom.append(v_bot)

    for v in ring_top:
        bm.faces.new([top_center, v, ring_top[(ring_top.index(v)+1)%steps]])

    for i in range(steps):
        v1 = ring_top[i]
        v2 = ring_top[(i+1)%steps]
        v3 = ring_bottom[(i+1)%steps]
        v4 = ring_bottom[i]
        bm.faces.new([v1, v2, v3, v4])

    for v in ring_bottom:
        bm.faces.new([v, bottom, ring_bottom[(ring_bottom.index(v)+1)%steps]])

    bm.to_mesh(mesh)
    bm.free()

    bpy.ops.object.shade_smooth()
    return obj

def create_capsule():
    bpy.ops.mesh.primitive_cylinder_add(radius=0.05, depth=0.1)
    obj = bpy.context.object
    return obj

def get_scale_factor(size_option):
    if size_option == 'SMALL':
        return 0.6
    elif size_option == 'MEDIUM':
        return 0.8
    elif size_option == 'LARGE':
        return 1.0
    elif size_option == 'MIXED':
        return random.choice([0.6, 0.8, 1.0])
    else:
        return 0.6

def create_particle_pair(index, shape_type, color):
    angle = random.uniform(0, 2 * math.pi)
    speed_xy = random.uniform(1.5, 2.5)
    speed_z = random.uniform(2.0, 3.0)

    t_peak = 5
    t_total = 20
    start = (0, 0, 0)
    peak = (
        math.cos(angle) * speed_xy,
        math.sin(angle) * speed_xy,
        speed_z
    )
    land = (
        math.cos(angle) * speed_xy * (t_total / t_peak),
        math.sin(angle) * speed_xy * (t_total / t_peak),
        0
    )

    def make_shape(name, use_color=False):
        if shape_type == 'SPHERE':
            bpy.ops.mesh.primitive_uv_sphere_add(radius=0.05, location=start)
            obj = bpy.context.object
        elif shape_type == 'STAR':
            obj = create_star()
        elif shape_type == 'CUBE':
            bpy.ops.mesh.primitive_cube_add(size=0.1, location=start)
            obj = bpy.context.object
        elif shape_type == 'CONE':
            bpy.ops.mesh.primitive_cone_add(radius1=0.07, depth=0.15, location=start)
            obj = bpy.context.object
        elif shape_type == 'HEART':
            obj = create_heart()
        elif shape_type == 'DIAMOND':
            obj = create_diamond()
        elif shape_type == 'CAPSULE':
            obj = create_capsule()
        else:
            bpy.ops.mesh.primitive_uv_sphere_add(radius=0.05, location=start)
            obj = bpy.context.object

        obj.name = f"{name}_{index}"

        scale_factor = get_scale_factor(bpy.context.scene.burst_size)
        obj.scale = (scale_factor, scale_factor, scale_factor)

        obj.location = start
        obj.keyframe_insert(data_path="location", frame=15)
        obj.location = peak
        obj.keyframe_insert(data_path="location", frame=20)
        obj.location = land
        obj.keyframe_insert(data_path="location", frame=35)

        if use_color:
            mat = bpy.data.materials.new(name=f"Mat_{index}")
            mat.use_nodes = True
            bsdf = mat.node_tree.nodes.get("Principled BSDF")
            if bsdf:
                bsdf.inputs["Base Color"].default_value = (color[0], color[1], color[2], 1.0)
            obj.data.materials.append(mat)

    make_shape("ParticleSphere", use_color=False)
    make_shape("ParticleShape", use_color=True)

def generate_effect(shape_type):
    clear_scene()
    create_falling_sphere()
    color = bpy.context.scene.burst_color
    for i in range(20):
        create_particle_pair(i, shape_type, color)

class OBJECT_OT_generate_shape_burst(bpy.types.Operator):
    bl_idname = "object.generate_shape_burst"
    bl_label = "Generate Shape Burst"
    bl_description = "Drop sphere and bounce selected shape with natural arc"

    def execute(self, context):
        generate_effect(context.scene.burst_shape)
        return {'FINISHED'}

class VIEW3D_PT_shape_burst_panel(bpy.types.Panel):
    bl_label = "Burst Shape Generator"
    bl_idname = "VIEW3D_PT_shape_burst_panel"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "Visual Effects"

    def draw(self, context):
        layout = self.layout
        layout.prop(context.scene, "burst_shape", text="Shape")
        layout.prop(context.scene, "burst_color", text="Shape Color")
        layout.prop(context.scene, "burst_size", text="Size")
        layout.operator("object.generate_shape_burst")

def register():
    bpy.utils.register_class(OBJECT_OT_generate_shape_burst)
    bpy.utils.register_class(VIEW3D_PT_shape_burst_panel)
    bpy.types.Scene.burst_shape = EnumProperty(
        name="Shape Type",
        items=[
            ('SPHERE', "Sphere", ""),
            ('STAR', "Star", ""),
            ('CUBE', "Cube", ""),
            ('CONE', "Cone", ""),
            ('HEART', "Heart", ""),
            ('DIAMOND', "Diamond", ""),
            ('CAPSULE', "Capsule", "")
        ],
        default='SPHERE'
    )
    bpy.types.Scene.burst_color = FloatVectorProperty(
        name="Color",
        subtype='COLOR',
        min=0.0, max=1.0,
        default=(1.0, 0.5, 1.0)
    )
    bpy.types.Scene.burst_size = EnumProperty(
        name="Size",
        items=[
            ('SMALL', "Small", ""),
            ('MEDIUM', "Medium", ""),
            ('LARGE', "Large", ""),
            ('MIXED', "Mix", "")
        ],
        default='SMALL'
    )

    clear_scene()  # 起動時に全オブジェクト削除

def unregister():
    bpy.utils.unregister_class(OBJECT_OT_generate_shape_burst)
    bpy.utils.unregister_class(VIEW3D_PT_shape_burst_panel)
    del bpy.types.Scene.burst_shape
    del bpy.types.Scene.burst_color
    del bpy.types.Scene.burst_size

if __name__ == "__main__":
    register()