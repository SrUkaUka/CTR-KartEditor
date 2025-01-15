import bpy
import os
from bpy.props import StringProperty
from bpy.types import Operator, Panel
from bpy_extras.io_utils import ImportHelper

image_height = 192  # Altura de la imagen original en píxeles

# Convertir coordenadas Y de GIMP a Blender
def convert_coords(coords):
    xmin, ymin, xmax, ymax = coords
    return (xmin, image_height - ymax, xmax, image_height - ymin)

# Nuevas coordenadas originales de GIMP para template08
gimp_coords_list = [
    (365, 43, 301, 111),    # kart_top
    (112, 87, 176, 119),    # kart_front_side
    (318, 10, 350, 14),     # kart_front_bottom
    (227, 40, 259, 44),     # kart_front_02
    (208, 10, 272, 14),     # kart_front
    (34, 88, 66, 120),      # kart_floor
    (118, 10, 166, 58),     # kart_back_bottom
    (28, 10, 76, 58),       # kart_back_02
    (395, 119, 443, 167),   # exhaust_pipe_02
    (405, 5, 437, 37),      # exhaust_pipe_01
    (405, 61, 437, 93),     # exhaust_pipe_00
    (95, 157, 127, 161),    # metal_01
    (157, 157, 189, 161),   # metal_02
    (211, 157, 275, 161),   # metal_04
    (32, 149, 64, 167),     # top
    (209, 75, 273, 91),     # tube
    (226, 115, 258, 119)    # tube_02
]

# Convertir coordenadas a formato Blender
crop_coords_list = [convert_coords(coords) for coords in gimp_coords_list]

crop_names = [
    "kart_top",
    "kart_front_side",
    "kart_front_bottom",
    "kart_front_02",
    "kart_front",
    "kart_floor",
    "kart_back_bottom",
    "kart_back_02",
    "exhaust_pipe_02",
    "exhaust_pipe_01",
    "exhaust_pipe_00",
    "metal_01",
    "metal_02",
    "metal_04",
    "top",
    "tube",
    "tube_02"
]

# Función para recortar una imagen
def crop_image(image, coords):
    xmin, ymin, xmax, ymax = coords
    width = xmax - xmin
    height = ymax - ymin
    
    if width <= 0 or height <= 0:
        print(f"Error: dimensiones de recorte inválidas para {image.name} ({coords})")
        return None
    
    # Crear una nueva imagen recortada
    image_cropped = bpy.data.images.new(image.name + "_cropped", width, height)
    
    # Copiar los píxeles recortados a la nueva imagen
    pixels = list(image.pixels)
    pixels_cropped = [0] * (width * height * 4)  # RGBA channels
    for y in range(height):
        for x in range(width):
            src_x = xmin + x
            src_y = ymin + y
            src_idx = (src_y * image.size[0] + src_x) * 4
            dest_idx = (y * width + x) * 4
            pixels_cropped[dest_idx:dest_idx + 4] = pixels[src_idx:src_idx + 4]
    
    # Asignar los píxeles a la imagen recortada
    image_cropped.pixels = pixels_cropped
    
    return image_cropped

# Función para procesar una imagen
def process_image(image_path, crop_coords, crop_name):
    # Cargar la imagen desde el path
    image = bpy.data.images.load(image_path)
    
    # Aplicar el recorte
    image_cropped = crop_image(image, crop_coords)
    
    if image_cropped is not None:
        # Guardar la imagen recortada en la misma carpeta de origen
        original_folder = os.path.dirname(image_path)
        cropped_image_path = os.path.join(original_folder, crop_name + ".png")
        image_cropped.filepath_raw = cropped_image_path
        image_cropped.file_format = 'PNG'  # Asegurarse de que sea PNG
        image_cropped.save()
        print(f"Imagen {crop_name}.png guardada en {original_folder}")

class OT_SelectMainFolder(Operator, ImportHelper):
    bl_idname = "file.select_main_folder"
    bl_label = "Select Main Folder"
    
    directory: StringProperty(
        name="Directory",
        description="Select the main folder",
        maxlen=1024,
        subtype='DIR_PATH',
    )
    
    def execute(self, context):
        main_folder = self.directory
        print(f"Selected main folder: {main_folder}")
        
        # Recorrer todas las subcarpetas dentro de la carpeta principal
        for root, dirs, files in os.walk(main_folder):
            found_images = []
            for file in files:
                if file.lower().startswith("template08"):
                    found_images.append(file)
                    image_path = os.path.join(root, file)
                    
                    # Procesar la imagen para cada juego de coordenadas
                    for coords, name in zip(crop_coords_list, crop_names):
                        process_image(image_path, coords, name)
                else:
                    # Eliminar otras imágenes
                    file_path = os.path.join(root, file)
                    os.remove(file_path)
                    print(f"Imagen {file} eliminada de {root}")

            if not found_images:
                print(f"No se encontraron imágenes 'template08' en {root}")

        print("Proceso completado.")
        return {'FINISHED'}

class OT_CleanTextures(Operator):
    bl_idname = "object.clean_textures"
    bl_label = "Clean Textures"
    
    def execute(self, context):
        bpy.ops.file.select_main_folder('INVOKE_DEFAULT')
        return {'FINISHED'}

class PT_MainPanel(Panel):
    bl_idname = "PT_MainPanel"
    bl_label = "Clean Textures Panel"
    bl_category = "Clean Textures"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    
    def draw(self, context):
        layout = self.layout
        layout.operator("object.clean_textures", text="Clean Textures")

def register():
    bpy.utils.register_class(OT_SelectMainFolder)
    bpy.utils.register_class(OT_CleanTextures)
    bpy.utils.register_class(PT_MainPanel)

def unregister():
    bpy.utils.unregister_class(OT_SelectMainFolder)
    bpy.utils.unregister_class(OT_CleanTextures)
    bpy.utils.unregister_class(PT_MainPanel)

if __name__ == "__main__":
    register()
