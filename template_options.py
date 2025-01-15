import bpy
import os

# Especifica la ruta de la carpeta que contiene los scripts
scripts_folder = r"C:\Users\Kevin\Desktop\Kevin\kart_editor\ctr-kart-editor\ctr-kart-editor-master\kart_master"

# Función para abrir y ejecutar un script en el Editor de Texto de Blender
def open_and_execute_script(script_name):
    script_path = os.path.join(scripts_folder, script_name)
    if os.path.exists(script_path):
        bpy.ops.text.open(filepath=script_path)
        text_block = bpy.data.texts[script_name]
        bpy.ops.text.run_script({'edit_text': text_block})
    else:
        print(f"El script {script_name} no existe en la carpeta {scripts_folder}")

# Definir las operaciones de botones
class EXECUTE_OT_kart_template(bpy.types.Operator):
    bl_idname = "wm.execute_kart_template"
    bl_label = "Ejecutar Kart Template"
    
    def execute(self, context):
        scripts = ["kart_editor.py", "kart_clean_textures.py", "16_color_reset.py"]
        for script in scripts:
            open_and_execute_script(script)
        return {'FINISHED'}

class EXECUTE_OT_hi_kart_template(bpy.types.Operator):
    bl_idname = "wm.execute_hi_kart_template"
    bl_label = "Ejecutar Hi Kart Template"
    
    def execute(self, context):
        scripts = ["hi_kart_editor.py", "hi_kart_clean_textures.py", "16_color_reset.py"]
        for script in scripts:
            open_and_execute_script(script)
        return {'FINISHED'}

class EXECUTE_OT_velo_chopper_template(bpy.types.Operator):
    bl_idname = "wm.execute_velo_chopper_template"
    bl_label = "Ejecutar Velo Chopper Template"
    
    def execute(self, context):
        scripts = ["velo_chopper_editor.py", "velo_chopper_clean_textures.py", "16_color_reset.py"]
        for script in scripts:
            open_and_execute_script(script)
        return {'FINISHED'}

class EXECUTE_OT_hovercraft_template(bpy.types.Operator):
    bl_idname = "wm.execute_hovercraft_template"
    bl_label = "Ejecutar Hovercraft Template"
    
    def execute(self, context):
        scripts = ["hovercraft_editor.py"]
        for script in scripts:
            open_and_execute_script(script)
        return {'FINISHED'}

# Definir el panel en Blender
class CUSTOM_PT_script_panel(bpy.types.Panel):
    bl_label = "Panel de Ejecución de Scripts"
    bl_idname = "CUSTOM_PT_script_panel"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'Template_Options'
    
    def draw(self, context):
        layout = self.layout
        layout.operator("wm.execute_kart_template")
        layout.operator("wm.execute_hi_kart_template")
        layout.operator("wm.execute_velo_chopper_template")
        layout.operator("wm.execute_hovercraft_template")

# Registrar las clases en Blender
classes = [
    EXECUTE_OT_kart_template,
    EXECUTE_OT_hi_kart_template,
    EXECUTE_OT_velo_chopper_template,
    EXECUTE_OT_hovercraft_template,
    CUSTOM_PT_script_panel,
]

def register():
    for cls in classes:
        bpy.utils.register_class(cls)

def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)

if __name__ == "__main__":
    register()
