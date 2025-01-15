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
        fbx_directory = "C:/Users/Kevin/Desktop/Kevin\kart_editor/ctr-kart-editor/kart_fbx"
        fbx_file = os.path.join(fbx_directory, "kart_template.fbx")  # Ruta correcta del archivo .fbx
        
        # Importar el archivo .fbx
        bpy.ops.import_scene.fbx(filepath=fbx_file)

        # Encontrar el material adecuado con el prefijo "template" en modo de shading
        material_found = False
        for obj in bpy.context.scene.objects:
            if obj.type == 'MESH':
                for slot in obj.material_slots:
                    if slot.material and slot.material.use_nodes and slot.material.name.startswith("template"):
                        material = slot.material
                        material_found = True
                        break
                if material_found:
                    break

        if not material_found:
            self.report({'ERROR'}, "No se encontró ningún material con el prefijo 'template' y nodos de shading habilitados en los objetos.")
            return {'CANCELLED'}

        # Limpiar todos los nodos existentes en el material
        material.use_nodes = True
        nodes = material.node_tree.nodes
        links = material.node_tree.links

        # Eliminar todos los nodos existentes
        for node in nodes:
            nodes.remove(node)

        # Crear nodo Image Texture para template01 o template05 según la opción seleccionada
        selected_option = context.scene.template_option
        if selected_option in {'GOLD_PIPES', 'SILVER_PIPES'}:
            image_path1 = os.path.join(fbx_directory, "template05.png")
        else:
            image_path1 = os.path.join(fbx_directory, "template01.png")

        node_image1 = nodes.new(type='ShaderNodeTexImage')
        node_image1.location = (-800, 200)
        image_texture1 = bpy.data.images.load(image_path1)
        node_image1.image = image_texture1

        # Crear nodo Overlay para template01 o template05
        node_overlay1 = nodes.new(type='ShaderNodeMixRGB')
        node_overlay1.location = (-200, 200)
        node_overlay1.blend_type = 'OVERLAY'
        node_overlay1.inputs[0].default_value = 1.0  # Fac = 1.000

        # Crear nodo RGB1 para template01 o template05
        node_rgb1 = nodes.new(type='ShaderNodeRGB')
        node_rgb1.location = (-400, 200)
        node_rgb1.outputs[0].default_value = (1.0, 1.0, 1.0, 1.0)  # Color blanco
        
        # Crear nodo MixShader1
        node_mix_shader1 = nodes.new(type='ShaderNodeMixShader')
        node_mix_shader1.location = (0, 200)
        node_mix_shader1.inputs[0].default_value = 0  # Fac = 0.500
        
        # Crear nodo AddShader1
        node_add_shader1 = nodes.new(type='ShaderNodeAddShader')
        node_add_shader1.location = (400, 0)
        node_add_shader1.inputs[0]    

        # Crear nodo Overlay para template01 o template05
        node_overlay1 = nodes.new(type='ShaderNodeMixRGB')
        node_overlay1.location = (-200, 200)
        node_overlay1.blend_type = 'OVERLAY'
        node_overlay1.inputs[0].default_value = 1.0  # Fac = 1.000

        # Conectar Image Texture a Overlay
        links.new(node_image1.outputs['Color'], node_overlay1.inputs[1])

        # Crear nodo RGB1 para template01 o template05
        node_rgb1 = nodes.new(type='ShaderNodeRGB')
        node_rgb1.location = (-400, 200)
        node_rgb1.outputs[0].default_value = (1.0, 1.0, 1.0, 1.0)  # Color blanco
        
        # Crear nodo MixShader1
        node_mix_shader1 = nodes.new(type='ShaderNodeMixShader')
        node_mix_shader1.location = (0, 200)
        node_mix_shader1.inputs[0].default_value = 0  # Fac = 0.500
        
        # Crear nodo AddShader2
        node_add_shader2 = nodes.new(type='ShaderNodeAddShader')
        node_add_shader2.location = (800, 0)
        node_add_shader2.inputs[0]
        
        # Crear nodo Material Output
        node_material_output = nodes.new(type='ShaderNodeOutputMaterial')
        node_material_output.location = (1000, 0)
        
        # Conectar Image Texture a Overlay
        links.new(node_image1.outputs['Color'], node_overlay1.inputs[1])
        
        # Conectar RGB a Overlay en Color2
        links.new(node_rgb1.outputs['Color'], node_overlay1.inputs[2])
        
        # Conectar Overlay a Mix Shader
        links.new(node_overlay1.outputs['Color'], node_mix_shader1.inputs[1])
        
        # Conectar Mix Shader a Add Shader1
        links.new(node_mix_shader1.outputs['Shader'], node_add_shader1.inputs[0])
        
        # Conectar Add Shader1 a Add Shader2
        links.new(node_add_shader1.outputs['Shader'], node_add_shader2.inputs[0])
        
        # Conectar Add Shader2 a Material Output
        links.new(node_add_shader2.outputs['Shader'],  node_material_output.inputs[0])
        
        # Crear nodo Image Texture para template02/03/04
        if selected_option == 'DEFAULT':
            image_path2 = os.path.join(fbx_directory, "template02.png")
        elif selected_option == 'GOLD_PIPES':
            image_path2 = os.path.join(fbx_directory, "template03.png")
        elif selected_option == 'SILVER_PIPES':
            image_path2 = os.path.join(fbx_directory, "template04.png")
        else:
            # Opción por defecto (DEFAULT)
            image_path2 = os.path.join(fbx_directory, "template02.png")

        node_image2 = nodes.new(type='ShaderNodeTexImage')
        node_image2.location = (-800, -200)
        image_texture2 = bpy.data.images.load(image_path2)
        node_image2.image = image_texture2
        
        # Crear nodo RGB2 
        node_rgb2 = nodes.new(type='ShaderNodeRGB')
        node_rgb2.location = (-400, -200)
        node_rgb2.outputs[0].default_value = (1.0, 1.0, 1.0, 1.0)  # Color blanco
        
        # Crear nodo overlay para template02/03/04
        node_overlay2 = nodes.new(type='ShaderNodeMixRGB')
        node_overlay2.location = (-200, -200)
        node_overlay2.blend_type = 'OVERLAY'
        node_overlay2.inputs[0].default_value = 1.0  # Fac = 1.000
        
        # Crear nodo MixShader2
        node_mix_shader2 = nodes.new(type='ShaderNodeMixShader')
        node_mix_shader2.location = (0, -200)
        node_mix_shader2.inputs[0].default_value = 0  # Fac = 0.500
        
        # Crear nodo AddShader3
        node_add_shader3 = nodes.new(type='ShaderNodeAddShader')
        node_add_shader3.location = (400, -800)
        node_add_shader3.inputs[0]   
        
        # Conectar Image Texture a Overlay
        links.new(node_image2.outputs['Color'], node_overlay2.inputs[1])
        
        # Conectar RGB a Overlay en Color2
        links.new(node_rgb2.outputs['Color'], node_overlay2.inputs[2])
        
        # Conectar Overlay a Mix Shader
        links.new(node_overlay2.outputs['Color'], node_mix_shader2.inputs[1])
        
        # Conectar Mix Shader a Add Shader1
        links.new(node_mix_shader2.outputs['Shader'], node_add_shader1.inputs[1])
                
        # Crear nodo Image Texture para template06
        image_path6 = os.path.join(fbx_directory, "template06.png")
        node_image6 = nodes.new(type='ShaderNodeTexImage')
        node_image6.location = (-800, -600)
        image_texture6 = bpy.data.images.load(image_path6)
        node_image6.image = image_texture6
        
        # Crear nodo RGB3 
        node_rgb3 = nodes.new(type='ShaderNodeRGB')
        node_rgb3.location = (-400, -600)
        node_rgb3.outputs[0].default_value = (1.0, 1.0, 1.0, 1.0)  # Color blanco
        
        # Crear nodo overlay para template02/03/04
        node_overlay3 = nodes.new(type='ShaderNodeMixRGB')
        node_overlay3.location = (-200, -600)
        node_overlay3.blend_type = 'OVERLAY'
        node_overlay3.inputs[0].default_value = 1.0  # Fac = 1.000
        
        # Crear nodo MixShader3
        node_mix_shader3 = nodes.new(type='ShaderNodeMixShader')
        node_mix_shader3.location = (0, -600)
        node_mix_shader3.inputs[0].default_value = 0.300  # Fac = 0.500
        
        # Conectar Image Texture a Overlay
        links.new(node_image6.outputs['Color'], node_overlay3.inputs[1])
        
        # Conectar RGB a Overlay en Color2
        links.new(node_rgb3.outputs['Color'], node_overlay3.inputs[2])
        
        # Conectar Overlay a Mix Shader
        links.new(node_overlay3.outputs['Color'], node_mix_shader3.inputs[1])
        
        # Conectar Mix Shader a Add Shader1
        links.new(node_mix_shader3.outputs['Shader'], node_add_shader3.inputs[0])
        
        # Conectar Mix Shader a Add Shader1
        links.new(node_add_shader3.outputs['Shader'], node_add_shader2.inputs[1])
        
        # Crear nodo Image Texture para template07
        image_path7 = os.path.join(fbx_directory, "template07.png")
        node_image7 = nodes.new(type='ShaderNodeTexImage')
        node_image7.location = (-800, -1000)
        image_texture7 = bpy.data.images.load(image_path7)
        node_image7.image = image_texture7
        
        # Crear nodo RGB4 
        node_rgb4 = nodes.new(type='ShaderNodeRGB')
        node_rgb4.location = (-400, -1000)
        node_rgb4.outputs[0].default_value = (1.0, 1.0, 1.0, 1.0)  # Color blanco
        
        # Crear nodo overlay para template 07
        node_overlay4 = nodes.new(type='ShaderNodeMixRGB')
        node_overlay4.location = (-200, -1000)
        node_overlay4.blend_type = 'OVERLAY'
        node_overlay4.inputs[0].default_value = 1.0  # Fac = 1.000
        
        # Crear nodo MixShader4
        node_mix_shader4 = nodes.new(type='ShaderNodeMixShader')
        node_mix_shader4.location = (0, -1000)
        node_mix_shader4.inputs[0].default_value = 0.300  # Fac = 0.500
        
        # Conectar Image Texture a Overlay4
        links.new(node_image7.outputs['Color'], node_overlay4.inputs[1])
        
        # Conectar RGB4 a Overlay en Color2
        links.new(node_rgb4.outputs['Color'], node_overlay4.inputs[2])
        
        # Conectar Overlay4 a Mix Shader
        links.new(node_overlay4.outputs['Color'], node_mix_shader4.inputs[1])
        
        # Conectar Mix Shader4 a Add Shader1
        links.new(node_mix_shader4.outputs['Shader'], node_add_shader3.inputs[1])
        
        # Conectar Mix Shader4 a Add Shader1
        links.new(node_add_shader3.outputs['Shader'], node_add_shader2.inputs[1])
                
        return {'FINISHED'}

class SetTemplateOptionOperator(bpy.types.Operator):
    """Define la opción de template seleccionada"""
    bl_idname = "wm.set_template_option"
    bl_label = "Set Template Option"

    option: bpy.props.EnumProperty(
        name="Template Option",
        description="Selecciona la opción de template",
        items=[
            ('NONE', "Seleccionar", "Seleccionar una opción de template"),
            ('DEFAULT', "Default", "Template Default"),
            ('GOLD_PIPES', "Gold pipes", "Gold pipes"),
            ('SILVER_PIPES', "Silver pipes", "Silver pipes")
        ]
    )

    def execute(self, context):
        context.scene.template_option = self.option
        return {'FINISHED'}

class BakeTexturesOperator(bpy.types.Operator):
    """Configura la escena y realiza el bake de texturas"""
    bl_idname = "wm.bake_textures"
    bl_label = "Bake Textures"

    def execute(self, context):
        # Configurar la escena para renderizar en Cycles y bake de texturas
        bpy.context.scene.render.engine = 'CYCLES'
        bpy.context.scene.cycles.device = 'GPU'
        bpy.context.scene.cycles.samples = 32

        # Desactivar direct e indirect lighting para el bake
        bpy.context.scene.render.bake.use_pass_direct = False
        bpy.context.scene.render.bake.use_pass_indirect = False

        # Seleccionar el objeto activo para asegurar el contexto correcto
        bpy.context.view_layer.objects.active = bpy.context.scene.objects.get("kart_template")

        # Realizar el bake
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
        # Obtener la carpeta de exportación seleccionada por el usuario
        export_directory = context.scene.export_folder

        if not export_directory:
            self.report({'ERROR'}, "Debes seleccionar una carpeta de exportación.")
            return {'CANCELLED'}

        # Iterar sobre todas las imágenes en el proyecto y exportarlas
        for img in bpy.data.images:
            if img.is_dirty:
                img.file_format = 'PNG'  # O el formato de archivo deseado
                img.save_render(os.path.join(export_directory, f"{img.name}.png"))

        self.report({'INFO'}, f"¡Se han exportado las texturas correctamente a {export_directory}!")

        return {'FINISHED'}

class CustomPanel(bpy.types.Panel):
    """Panel personalizado para configurar el template"""
    bl_label = "Template Options"
    bl_idname = "PT_CustomPanel"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'Kart_Edit'

    def draw(self, context):
        layout = self.layout
        scene = context.scene

        # Selector de opciones para el template
        layout.label(text="Select Template Option:")
        layout.prop(scene, "template_option", text="")

        # Botones para importar template, bake de texturas y exportar texturas
        layout.operator("wm.import_template", text="Import Template")
        layout.operator("wm.bake_textures", text="Bake Textures")
        
        # Selector de carpeta de exportación
        row = layout.row()
        row.label(text="Export Folder:")
        row.prop(context.scene, "export_folder", text="")
        row.operator("wm.select_export_folder", text="Select", icon='FILE_FOLDER')
        
        layout.operator("wm.export_textures", text="Export Textures")

def register():
    bpy.utils.register_class(ImportTemplateOperator)
    bpy.utils.register_class(SetTemplateOptionOperator)
    bpy.utils.register_class(BakeTexturesOperator)
    bpy.utils.register_class(SelectExportFolderOperator)
    bpy.utils.register_class(ExportTexturesOperator)
    bpy.utils.register_class(CustomPanel)

    bpy.types.Scene.template_option = bpy.props.EnumProperty(
        name="Template Option",
        description="Select template option",
        items=[
            ('NONE', "Seleccionar", "Seleccionar una opción de template"),
            ('DEFAULT', "Default", "Template Default"),
            ('GOLD_PIPES', "Gold pipes", "Gold pipes"),
            ('SILVER_PIPES', "Silver pipes", "Silver pipes")
        ],
        default='NONE'
    )

    bpy.types.Scene.export_folder = bpy.props.StringProperty(
        name="Export Folder",
        description="Folder for exporting textures",
        subtype='DIR_PATH'
    )

def unregister():
    bpy.utils.unregister_class(ImportTemplateOperator)
    bpy.utils.unregister_class(SetTemplateOptionOperator)
    bpy.utils.unregister_class(BakeTexturesOperator)
    bpy.utils.unregister_class(SelectExportFolderOperator)
    bpy.utils.unregister_class(ExportTexturesOperator)
    bpy.utils.unregister_class(CustomPanel)

    del bpy.types.Scene.template_option
    del bpy.types.Scene.export_folder

if __name__ == "__main__":
    register()
