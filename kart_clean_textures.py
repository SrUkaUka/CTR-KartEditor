import bpy
import os
from bpy.props import StringProperty
from bpy.types import Operator, Panel
from bpy_extras.io_utils import ImportHelper

image_height = 107  # Altura de la imagen original en píxeles

# Convertir coordenadas Y de GIMP a Blender
def convert_coords(coords):
    xmin, ymin, xmax, ymax = coords
    return (xmin, image_height - ymax, xmax, image_height - ymin)

# Coordenadas originales de GIMP
gimp_coords_list = [
    (3, 3, 35, 19),    # Coordenadas para "Front"
    (38, 3, 70, 19),   # Coordenadas para "Back"
    (82, 3, 98, 19),   # Coordenadas para "Bridge"
    (12, 41, 28, 49),  # Coordenadas para "Floor"
    (46, 43, 62, 47),  # Coordenadas para "Red"
    (82, 38, 98, 54),  # Coordenadas para "Exhaust"
    (7, 71, 39, 87),   # Coordenadas para "Motortop"
    (64, 71, 96, 87),  # Coordenadas para "Side"
    (46, 89, 62, 105)  # Coordenadas para "Exhaust Pipe"
]

# Convertir coordenadas a formato Blender
crop_coords_list = [convert_coords(coords) for coords in gimp_coords_list]

crop_names = [
    "front",
    "back",
    "bridge",
    "floor",
    "red",
    "exhaust",
    "motortop",
    "side",
    "exhaust_pipe"
]

# Función para recortar una imagen
def crop_image(image, coords):
    xmin, ymin, xmax, ymax = coords
    width = xmax - xmin
    height = ymax - ymin
    
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
            pixels_cropped[dest_idx:dest_idx+4] = pixels[src_idx:src_idx+4]
    
    # Asignar los píxeles a la imagen recortada
    image_cropped.pixels = pixels_cropped
    
    return image_cropped

# Función para procesar una imagen
def process_image(image_path, crop_coords, crop_name):
    # Cargar la imagen desde el path
    image = bpy.data.images.load(image_path)
    
    # Aplicar el recorte
    image_cropped = crop_image(image, crop_coords)
    
    # Guardar la imagen recortada en la misma carpeta de origen
    original_folder = os.path.dirname(image_path)
    cropped_image_path = os.path.join(original_folder, crop_name + ".png")
    image_cropped.filepath_raw = cropped_image_path
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
                if file.lower().startswith("template01") or file.lower().startswith("template05"):
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
                print(f"No se encontraron imágenes 'template01' o 'template05' en {root}")

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
