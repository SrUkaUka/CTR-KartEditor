import bpy
import os

class ImportTemplateOperator(bpy.types.Operator):
    """Importa el archivo .fbx y configura los nodos de textura"""
    bl_idname = "wm.import_template"
    bl_label = "Import Template"

    def execute(self, context):
        # Verificar que se haya seleccionado una opción válida
        if context.scene.template_option == 'NONE':
            self.report({'ERROR'}, "Debes seleccionar una opción antes de importar el template.")
            return {'CANCELLED'}

        # Directorio donde se encuentra el archivo .fbx y las imágenes
        fbx_directory = r"C:\Users\Kevin\Desktop\Kevin\kart_editor\ctr-kart-editor\hi_kart_fbx"
        fbx_file = os.path.join(fbx_directory, "hi_kart_template.fbx")
        
        # Importar el archivo .fbx
        bpy.ops.import_scene.fbx(filepath=fbx_file)

        # Encontrar el material adecuado
        material_found = False
        for obj in bpy.context.scene.objects:
            if obj.type == 'MESH':
                for slot in obj.material_slots:
                    if slot.material and slot.material.use_nodes and slot.material.name.startswith("hi_kart_template"):
                        material = slot.material
                        material_found = True
                        break
                if material_found:
                    break

        if not material_found:
            self.report({'ERROR'}, "No se encontró ningún material con el prefijo 'hi_kart_template'.")
            return {'CANCELLED'}

        # Limpiar nodos existentes en el material
        material.use_nodes = True
        nodes = material.node_tree.nodes
        links = material.node_tree.links

        for node in nodes:
            nodes.remove(node)

        # Configuración de nodos de textura
        selected_option = context.scene.template_option
        image_path1_1 = os.path.join(fbx_directory, "template08.png")
        image_path1_2 = os.path.join(fbx_directory, "template09.png")

        # Crear nodos
        node_image1_1 = nodes.new(type='ShaderNodeTexImage')
        node_image1_1.location = (-800, 200)
        node_image1_1.image = bpy.data.images.load(image_path1_1)

        node_overlay1_1 = nodes.new(type='ShaderNodeMixRGB')
        node_overlay1_1.location = (-600, 200)
        node_overlay1_1.blend_type = 'OVERLAY'
        node_overlay1_1.inputs[0].default_value = 1.0

        links.new(node_image1_1.outputs['Color'], node_overlay1_1.inputs[1])

        node_rgb1_1 = nodes.new(type='ShaderNodeRGB')
        node_rgb1_1.location = (-400, 200)
        node_rgb1_1.outputs[0].default_value = (1.0, 1.0, 1.0, 1.0)

        links.new(node_rgb1_1.outputs['Color'], node_overlay1_1.inputs[2])

        node_image1_2 = nodes.new(type='ShaderNodeTexImage')
        node_image1_2.location = (-800, 0)
        node_image1_2.image = bpy.data.images.load(image_path1_2)

        node_overlay1_2 = nodes.new(type='ShaderNodeMixRGB')
        node_overlay1_2.location = (-600, 0)
        node_overlay1_2.blend_type = 'OVERLAY'
        node_overlay1_2.inputs[0].default_value = 1.0

        links.new(node_image1_2.outputs['Color'], node_overlay1_2.inputs[1])

        node_rgb1_2 = nodes.new(type='ShaderNodeRGB')
        node_rgb1_2.location = (-400, 0)
        node_rgb1_2.outputs[0].default_value = (1.0, 1.0, 1.0, 1.0)

        links.new(node_rgb1_2.outputs['Color'], node_overlay1_2.inputs[2])

        # Configuración de la segunda textura según la opción
        if selected_option == 'DEFAULT':
            image_path2 = os.path.join(fbx_directory, "template010.png")
        elif selected_option == 'GOLD_PIPES':
            image_path2 = os.path.join(fbx_directory, "template011.png")
        else:
            image_path2 = os.path.join(fbx_directory, "template012.png")

        node_image2 = nodes.new(type='ShaderNodeTexImage')
        node_image2.location = (-600, -200)
        node_image2.image = bpy.data.images.load(image_path2)

        node_overlay3 = nodes.new(type='ShaderNodeMixRGB')
        node_overlay3.location = (-400, -200)
        node_overlay3.blend_type = 'OVERLAY'
        node_overlay3.inputs[0].default_value = 1.0

        links.new(node_image2.outputs['Color'], node_overlay3.inputs[1])

        node_rgb2 = nodes.new(type='ShaderNodeRGB')
        node_rgb2.location = (-200, -200)
        node_rgb2.outputs[0].default_value = (1.0, 1.0, 1.0, 1.0)

        links.new(node_rgb2.outputs['Color'], node_overlay3.inputs[2])

        # Salida del material
        node_output = nodes.new(type='ShaderNodeOutputMaterial')
        node_output.location = (800, 0)
        
        # Crear nodo MixShader1
        node_mix_shader1 = nodes.new(type='ShaderNodeMixShader')
        node_mix_shader1.location = (0, 200)
        node_mix_shader1.inputs[0].default_value = 0  # Fac = 0.000
        
        # Crear nodo MixShader2
        node_mix_shader2 = nodes.new(type='ShaderNodeMixShader')
        node_mix_shader2.location = (0, 0)
        node_mix_shader2.inputs[0].default_value = 0.300  # Fac = 0.300
        
        # Crear nodo MixShader3
        node_mix_shader3 = nodes.new(type='ShaderNodeMixShader')
        node_mix_shader3.location = (0, -200)
        node_mix_shader3.inputs[0].default_value = 0.300  # Fac = 0.300
        
        # Crear nodo AddShader1
        node_add_shader1 = nodes.new(type='ShaderNodeAddShader')
        node_add_shader1.location = (400, 0)
        node_add_shader1.inputs[0]
        
        # Crear nodo AddShader2
        node_add_shader2 = nodes.new(type='ShaderNodeAddShader')
        node_add_shader2.location = (400, -200)
        node_add_shader2.inputs[0]
        
        # Conectar Overlay1 a Mix Shader1
        links.new(node_overlay1_1.outputs['Color'], node_mix_shader1.inputs[1])
        
        # Conectar Overlay2 a Mix Shader2
        links.new(node_overlay1_2.outputs['Color'], node_mix_shader2.inputs[1])
        
        # Conectar Overlay3 a Mix Shader3
        links.new(node_overlay3.outputs['Color'], node_mix_shader3.inputs[1])
        
        # Conectar Mix Shader1 a Add Shader
        links.new(node_mix_shader1.outputs['Shader'], node_add_shader1.inputs[0])
        
        # Conectar Mix Shader2 a Add Shader
        links.new(node_mix_shader2.outputs['Shader'], node_add_shader1.inputs[1])
        
        # Conectar Mix Shader3 a Add Shader
        links.new(node_mix_shader3.outputs['Shader'], node_add_shader2.inputs[0])
        
        # Crear nodo Add Shader 3
        node_add_shader3 = nodes.new(type='ShaderNodeAddShader')
        node_add_shader3.location = (600,0)
        node_add_shader3.inputs[0]
        
        # Conectar Add Shader1 a Add Shader3
        links.new(node_add_shader1.outputs['Shader'], node_add_shader3.inputs[0])
        
        # Conectar Add Shader2 a Add Shader3
        links.new(node_add_shader2.outputs['Shader'], node_add_shader3.inputs[1])
        
        # Conectar Add Shader3 a Material Output
        links.new(node_add_shader3.outputs['Shader'], node_output.inputs[0])

        return {'FINISHED'}

class BakeTexturesOperator(bpy.types.Operator):
    """Configura la escena y realiza el bake de texturas"""
    bl_idname = "wm.bake_textures"
    bl_label = "Bake Textures"

    def execute(self, context):
        bpy.context.scene.render.engine = 'CYCLES'
        bpy.context.scene.cycles.device = 'GPU'
        bpy.context.scene.render.bake.use_pass_direct = False
        bpy.context.scene.render.bake.use_pass_indirect = False

        obj = bpy.context.view_layer.objects.active
        if obj is None or obj.type != 'MESH':
            self.report({'ERROR'}, "No se ha seleccionado un objeto válido para hacer bake.")
            return {'CANCELLED'}

        bpy.ops.object.bake(type='COMBINED')
        return {'FINISHED'}

class SelectExportFolderOperator(bpy.types.Operator):
    """Selecciona la carpeta de exportación para las texturas"""
    bl_idname = "wm.select_export_folder"
    bl_label = "Select Export Folder"

    filepath: bpy.props.StringProperty(subtype='DIR_PATH')

    def execute(self, context):
        context.scene.export_folder = self.filepath
        return {'FINISHED'}

class ExportTexturesOperator(bpy.types.Operator):
    """Exporta las texturas"""
    bl_idname = "wm.export_textures"
    bl_label = "Export Textures"

    def execute(self, context):
        export_directory = context.scene.export_folder

        if not export_directory:
            self.report({'ERROR'}, "Debes seleccionar una carpeta de exportación.")
            return {'CANCELLED'}

        for img in bpy.data.images:
            if img.is_dirty:
                img.file_format = 'PNG'
                img.save_render(os.path.join(export_directory, f"{img.name}.png"))

        self.report({'INFO'}, f"¡Se han exportado las texturas correctamente a {export_directory}!")
        return {'FINISHED'}

class SetTemplateOptionOperator(bpy.types.Operator):
    """Define la opción de template seleccionada"""
    bl_idname = "wm.set_template_option"
    bl_label = "Set Template Option"
    bl_options = {'REGISTER', 'UNDO'}

    template_option: bpy.props.EnumProperty(
        name="Template Option",
        description="Selecciona la opción de template",
        items=[
            ('DEFAULT', "Default", ""),
            ('GOLD_PIPES', "Gold Pipes", ""),
            ('SILVER_PIPES', "Silver Pipes", "")
        ]
    )

    def execute(self, context):
        context.scene.template_option = self.template_option
        self.report({'INFO'}, f"Opción de template establecida a: {self.template_option}")
        return {'FINISHED'}

class CustomPanel(bpy.types.Panel):
    """Panel personalizado para configurar el template y las texturas"""
    bl_label = "Template Options"
    bl_idname = "PT_CustomPanel"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'Kart_Edit'

    def draw(self, context):
        layout = self.layout
        scene = context.scene

        layout.label(text="Export Folder:")
        layout.prop(scene, "export_folder", text="")
        layout.operator("wm.select_export_folder", text="Select", icon='FILE_FOLDER')

        layout.label(text="Template Option:")
        layout.prop(scene, "template_option", text="")
        layout.operator("wm.set_template_option", text="Set Option")

        layout.operator("wm.import_template", text="Import Template")
        layout.operator("wm.bake_textures", text="Bake Textures")
        layout.operator("wm.export_textures", text="Export Textures")

def register():
    bpy.utils.register_class(ImportTemplateOperator)
    bpy.utils.register_class(BakeTexturesOperator)
    bpy.utils.register_class(SelectExportFolderOperator)
    bpy.utils.register_class(ExportTexturesOperator)
    bpy.utils.register_class(SetTemplateOptionOperator)
    bpy.utils.register_class(CustomPanel)

    bpy.types.Scene.export_folder = bpy.props.StringProperty(name="Export Folder", subtype='DIR_PATH')
    bpy.types.Scene.template_option = bpy.props.EnumProperty(
        name="Template Option",
        description="Selecciona la opción de template",
        items=[
            ('NONE', "None", ""),
            ('DEFAULT', "Default", ""),
            ('GOLD_PIPES', "Gold Pipes", ""),
            ('SILVER_PIPES', "Silver Pipes", "")
        ]
    )

def unregister():
    bpy.utils.unregister_class(ImportTemplateOperator)
    bpy.utils.unregister_class(BakeTexturesOperator)
    bpy.utils.unregister_class(SelectExportFolderOperator)
    bpy.utils.unregister_class(ExportTexturesOperator)
    bpy.utils.unregister_class(SetTemplateOptionOperator)
    bpy.utils.unregister_class(CustomPanel)

    del bpy.types.Scene.export_folder
    del bpy.types.Scene.template_option

if __name__ == "__main__":
    register()
