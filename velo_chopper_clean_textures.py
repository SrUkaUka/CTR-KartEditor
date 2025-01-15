import bpy
import os
from PIL import Image

# Coordenadas de Recorte
gimp_coords_list = [
    (8, 4, 28, 19),
    (67, 59, 79, 69),
    (11, 71, 18, 95),
    (36, 59, 52, 82),
    (158, 42, 178, 53),
    (39, 4, 68, 19),
    (27, 31, 59, 43),
    (108, 3, 124, 29),
    (134, 3, 149, 30),
    (127, 98, 135, 128),
    (78, 4, 101, 19),
    (2, 32, 25, 57),
    (165, 82, 173, 94),
    (129, 68, 133, 82),
    (68, 84, 79, 96),
    (43, 104, 47, 108),
    (159, 3, 176, 17),
    (3, 3, 35, 19),
    (116, 45, 142, 52),
    (96, 84, 102, 97),
    (77, 36, 91, 44)
]

template_names = [
    "back_00", "back_01", "chair_01", "exhaust_pipe01",
    "floor_01", "front_1", "front_2", "front_3",
    "front_4", "front_05", "front_06", "front_7",
    "motortop_01", "motortop_02", "pipe_03", "shadow_01",
    "side_1", "side_02", "side_02", "up_yellow", "left_right"
]

# Recorte de Imágenes
def crop_image(image_path, coords):
    img = Image.open(image_path)
    left, upper, right, lower = coords
    if left < right and upper < lower:
        cropped_img = img.crop((left, upper, right, lower))
        return cropped_img
    else:
        raise ValueError(f"Coordenadas inválidas: {coords}")

# Procesamiento de Imágenes
def process_image(image_path, crop_coords, crop_name):
    image = os.path.join(image_path, "template013.png")
    if os.path.exists(image):
        cropped = crop_image(image, crop_coords)
        cropped.save(os.path.join(image_path, f"{crop_name}.png"))
        print(f"Guardado: {crop_name}.png en {image_path}")  # Confirmación de guardado
    else:
        print(f"Archivo no encontrado: {image}")

# Propiedades de la escena
class MyProperties(bpy.types.PropertyGroup):
    my_folder_path: bpy.props.StringProperty(name="Folder Path", subtype='DIR_PATH')

# Operador para Limpiar Texturas
class OT_CleanTextures(bpy.types.Operator):
    bl_idname = "object.clean_textures"
    bl_label = "Clean Textures"

    def execute(self, context):
        main_folder = context.scene.my_properties.my_folder_path
        
        if not os.path.exists(main_folder):
            self.report({'WARNING'}, "La carpeta no existe.")
            return {'CANCELLED'}

        for root, dirs, files in os.walk(main_folder):
            template_file = os.path.join(root, "template013.png")
            if os.path.exists(template_file):
                for idx in range(len(gimp_coords_list)):
                    crop_coords = gimp_coords_list[idx]
                    crop_name = template_names[idx]
                    print(f"Recortando: {crop_name} usando {crop_coords}")  # Imprimir información del recorte
                    process_image(root, crop_coords, crop_name)

            # Eliminar otras imágenes en la carpeta
            for other_file in files:
                if not other_file.startswith("template013"):
                    os.remove(os.path.join(root, other_file))
        
        return {'FINISHED'}

# Panel en la Interfaz de Blender
class PT_MainPanel(bpy.types.Panel):
    bl_label = "Limpieza de Texturas"
    bl_idname = "PT_MainPanel"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "Clean Textures"

    def draw(self, context):
        layout = self.layout
        props = context.scene.my_properties
        
        layout.prop(props, "my_folder_path", text="Seleccionar Carpeta")
        layout.operator(OT_CleanTextures.bl_idname)

# Funciones de Registro y Anulación
def register():
    bpy.utils.register_class(MyProperties)
    bpy.types.Scene.my_properties = bpy.props.PointerProperty(type=MyProperties)
    bpy.utils.register_class(OT_CleanTextures)
    bpy.utils.register_class(PT_MainPanel)

def unregister():
    del bpy.types.Scene.my_properties
    bpy.utils.unregister_class(MyProperties)
    bpy.utils.unregister_class(OT_CleanTextures)
    bpy.utils.unregister_class(PT_MainPanel)

if __name__ == "__main__":
    register()
