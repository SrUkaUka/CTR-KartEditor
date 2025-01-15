import bpy
import os

class ImportTemplateOperator(bpy.types.Operator):
    """Importa el archivo .fbx y configura los nodos de textura"""
    bl_idname = "wm.import_template"
    bl_label = "Import Template"

    def execute(self, context):
        fbx_directory = "C:/Users/Kevin/Desktop/Kevin/kart_editor/ctr-kart-editor/velo_chopper_fbx"
        fbx_file = os.path.join(fbx_directory, "velo_chopper_template.fbx")

        if not os.path.exists(fbx_file):
            self.report({'ERROR'}, f"No se encontró el archivo: {fbx_file}")
            return {'CANCELLED'}

        bpy.ops.import_scene.fbx(filepath=fbx_file)

        material_found = False
        for obj in bpy.context.scene.objects:
            if obj.type == 'MESH':
                for slot in obj.material_slots:
                    if slot.material and slot.material.use_nodes and slot.material.name.startswith("velo_chopper_template"):
                        material = slot.material
                        material_found = True
                        break
                if material_found:
                    break

        if not material_found:
            self.report({'ERROR'}, "No se encontró ningún material adecuado.")
            return {'CANCELLED'}

        material.use_nodes = True
        nodes = material.node_tree.nodes
        links = material.node_tree.links

        # Limpiar nodos existentes
        for node in nodes:
            nodes.remove(node)

        templates = ["template013", "template014", "template015", "template016", "template017", "template018"]

        # Crear Mix Shaders
        mix_shader1 = nodes.new(type='ShaderNodeMixShader')
        mix_shader1.location = (0, 200)

        mix_shader2 = nodes.new(type='ShaderNodeMixShader')
        mix_shader2.location = (0, 0)

        mix_shader3 = nodes.new(type='ShaderNodeMixShader')
        mix_shader3.location = (0, -200)

        mix_shader4 = nodes.new(type='ShaderNodeMixShader')
        mix_shader4.location = (0, -400)

        mix_shader5 = nodes.new(type='ShaderNodeMixShader')
        mix_shader5.location = (0, -600)
        
        mix_shader6 = nodes.new(type='ShaderNodeMixShader')
        mix_shader6.location = (0, -800)
        
        # Crear nodo AddShader1
        node_add_shader1 = nodes.new(type='ShaderNodeAddShader')
        node_add_shader1.location = (400, 200)
        node_add_shader1.inputs[0]       

        # Crear nodo AddShader2
        node_add_shader2 = nodes.new(type='ShaderNodeAddShader')
        node_add_shader2.location = (400, 0)
        node_add_shader2.inputs[0]    

        # Crear nodo AddShader3
        node_add_shader3 = nodes.new(type='ShaderNodeAddShader')
        node_add_shader3.location = (700, 200)
        node_add_shader3.inputs[0]    

        # Crear nodo AddShader4
        node_add_shader4 = nodes.new(type='ShaderNodeAddShader')
        node_add_shader4.location = (900, 0)
        node_add_shader4.inputs[0]    

        # Crear nodo AddShader5
        node_add_shader5 = nodes.new(type='ShaderNodeAddShader')
        node_add_shader5.location = (700, -200)
        node_add_shader5.inputs[0]   
        
        # Crear nodo AddShader6
        node_add_shader6 = nodes.new(type='ShaderNodeAddShader')
        node_add_shader6.location = (400, -200)
        node_add_shader6.inputs[0]    
        
        # Crear nodo Overlay1
        node_overlay1 = nodes.new(type='ShaderNodeMixRGB')
        node_overlay1.location = (-150, 200)
        node_overlay1.blend_type = 'OVERLAY'
        node_overlay1.inputs[0].default_value = 1.0  # Fac = 1.000
        
        # Crear nodo Overlay2
        node_overlay2 = nodes.new(type='ShaderNodeMixRGB')
        node_overlay2.location = (-150, 0)
        node_overlay2.blend_type = 'OVERLAY'
        node_overlay2.inputs[0].default_value = 1.0  # Fac = 1.000
        
        # Crear nodo Overlay3
        node_overlay3 = nodes.new(type='ShaderNodeMixRGB')
        node_overlay3.location = (-150, -200)
        node_overlay3.blend_type = 'OVERLAY'
        node_overlay3.inputs[0].default_value = 1.0  # Fac = 1.000
                
        # Crear nodo Overlay4
        node_overlay4 = nodes.new(type='ShaderNodeMixRGB')
        node_overlay4.location = (-150, -400)
        node_overlay4.blend_type = 'OVERLAY'
        node_overlay4.inputs[0].default_value = 1.0  # Fac = 1.000
                        
        # Crear nodo Overlay5
        node_overlay5 = nodes.new(type='ShaderNodeMixRGB')
        node_overlay5.location = (-150, -600)
        node_overlay5.blend_type = 'OVERLAY'
        node_overlay5.inputs[0].default_value = 1.0  # Fac = 1.000
        
        # Crear nodo Overlay6
        node_overlay6 = nodes.new(type='ShaderNodeMixRGB')
        node_overlay6.location = (-150, -800)
        node_overlay6.blend_type = 'OVERLAY'
        node_overlay6.inputs[0].default_value = 1.0  # Fac = 1.000
        
        # Crear nodo RGB1
        node_rgb1 = nodes.new(type='ShaderNodeRGB')
        node_rgb1.location = (-350, 200)
        node_rgb1.outputs[0].default_value = (1.0, 1.0, 1.0, 1.0)  # Color blanco
        
        # Crear nodo RGB2
        node_rgb2 = nodes.new(type='ShaderNodeRGB')
        node_rgb2.location = (-350, 0)
        node_rgb2.outputs[0].default_value = (1.0, 1.0, 1.0, 1.0)  # Color blanco
        
        # Crear nodo RGB3
        node_rgb3 = nodes.new(type='ShaderNodeRGB')
        node_rgb3.location = (-350, -200)
        node_rgb3.outputs[0].default_value = (1.0, 1.0, 1.0, 1.0)  # Color blanco
        
        # Crear nodo RGB4
        node_rgb4 = nodes.new(type='ShaderNodeRGB')
        node_rgb4.location = (-350, -400)
        node_rgb4.outputs[0].default_value = (1.0, 1.0, 1.0, 1.0)  # Color blanco
        
         # Crear nodo RGB5
        node_rgb5 = nodes.new(type='ShaderNodeRGB')
        node_rgb5.location = (-350, -600)
        node_rgb5.outputs[0].default_value = (1.0, 1.0, 1.0, 1.0)  # Color blanco
        
        # Crear nodo RGB6
        node_rgb6 = nodes.new(type='ShaderNodeRGB')
        node_rgb6.location = (-350, -800)
        node_rgb6.outputs[0].default_value = (1.0, 1.0, 1.0, 1.0)  # Color blanco
        
        # Crear nodo Image Texture para template013
        image_path013 = os.path.join(fbx_directory, "template013.png")
        node_image013 = nodes.new(type='ShaderNodeTexImage')
        node_image013.location = (-600, 200)
        image_texture013 = bpy.data.images.load(image_path013)
        node_image013.image = image_texture013
        
        # Crear nodo Image Texture para template014
        image_path014 = os.path.join(fbx_directory, "template014.png")
        node_image014 = nodes.new(type='ShaderNodeTexImage')
        node_image014.location = (-600, 0)
        image_texture014 = bpy.data.images.load(image_path014)
        node_image014.image = image_texture014
        
        # Crear nodo Image Texture para template015
        image_path015 = os.path.join(fbx_directory, "template015.png")
        node_image015 = nodes.new(type='ShaderNodeTexImage')
        node_image015.location = (-600, -200)
        image_texture015 = bpy.data.images.load(image_path015)
        node_image015.image = image_texture015
        
        # Crear nodo Image Texture para template016
        image_path016 = os.path.join(fbx_directory, "template016.png")
        node_image016 = nodes.new(type='ShaderNodeTexImage')
        node_image016.location = (-600, -400)
        image_texture016 = bpy.data.images.load(image_path016)
        node_image016.image = image_texture016
        
        # Crear nodo Image Texture para template017
        image_path017 = os.path.join(fbx_directory, "template017.png")
        node_image017 = nodes.new(type='ShaderNodeTexImage')
        node_image017.location = (-600, -600)
        image_texture017 = bpy.data.images.load(image_path017)
        node_image017.image = image_texture017
        
        # Crear nodo Image Texture para template018
        image_path018 = os.path.join(fbx_directory, "template018.png")
        node_image018 = nodes.new(type='ShaderNodeTexImage')
        node_image018.location = (-600, -800)
        image_texture018 = bpy.data.images.load(image_path018)
        node_image018.image = image_texture018
        
        # Crear nodo Material Output
        node_material_output = nodes.new(type='ShaderNodeOutputMaterial')
        node_material_output.location = (1200, 0)
        
        # Conectar Image Texture13 a Overlay
        links.new(node_image013.outputs['Color'], node_overlay1.inputs[1])
        # Conectar Image Texture14 a Overlay
        links.new(node_image014.outputs['Color'], node_overlay2.inputs[1])
        # Conectar Image Texture15 a Overlay
        links.new(node_image015.outputs['Color'], node_overlay3.inputs[1])
        # Conectar Image Texture16 a Overlay
        links.new(node_image016.outputs['Color'], node_overlay4.inputs[1])
        # Conectar Image Texture17 a Overlay
        links.new(node_image017.outputs['Color'], node_overlay5.inputs[1])
        # Conectar Image Texture18 a Overlay
        links.new(node_image018.outputs['Color'], node_overlay6.inputs[1])
        
        # Conectar Overlay1 a Mix Shader 1
        links.new(node_overlay1.outputs['Color'], mix_shader1.inputs[1])
        # Conectar Overlay2 a Mix Shader 2
        links.new(node_overlay2.outputs['Color'], mix_shader2.inputs[1])
        # Conectar Overlay3 a Mix Shader 3
        links.new(node_overlay3.outputs['Color'], mix_shader3.inputs[1])
        # Conectar Overlay4 a Mix Shader 4
        links.new(node_overlay4.outputs['Color'], mix_shader4.inputs[1])
        # Conectar Overlay5 a Mix Shader 5
        links.new(node_overlay5.outputs['Color'], mix_shader5.inputs[1])
        # Conectar Overlay6 a Mix Shader 6
        links.new(node_overlay6.outputs['Color'], mix_shader6.inputs[1])
        
        # Conectar RGB1 a Overlay
        links.new(node_rgb1.outputs['Color'], node_overlay1.inputs[2])
        # Conectar RGB2 a Overlay
        links.new(node_rgb2.outputs['Color'], node_overlay2.inputs[2])
        # Conectar RGB3 a Overlay
        links.new(node_rgb3.outputs['Color'], node_overlay3.inputs[2])
        # Conectar RGB4 a Overlay
        links.new(node_rgb4.outputs['Color'], node_overlay4.inputs[2])
        # Conectar RGB5 a Overlay
        links.new(node_rgb5.outputs['Color'], node_overlay5.inputs[2])
        # Conectar RGB6 a Overlay
        links.new(node_rgb6.outputs['Color'], node_overlay6.inputs[2])
        
        # Conectar MixShader1 a Add Shader 1
        links.new(mix_shader1.outputs['Shader'], node_add_shader1.inputs[0])
        # Conectar MixShader2 a Add Shader 1
        links.new(mix_shader2.outputs['Shader'], node_add_shader1.inputs[1])
        # Conectar MixShader3 a Add Shader 2
        links.new(mix_shader3.outputs['Shader'], node_add_shader2.inputs[0])
        # Conectar MixShader4 a Add Shader 2
        links.new(mix_shader4.outputs['Shader'], node_add_shader2.inputs[1])
        # Conectar MixShader5 a Add Shader 3
        links.new(mix_shader5.outputs['Shader'], node_add_shader6.inputs[0])
        # Conectar MixShader5 a Add Shader 4
        links.new(mix_shader6.outputs['Shader'], node_add_shader6.inputs[1])
                
        # Conectar Add Shader 1 a Add Shader3
        links.new(node_add_shader1.outputs['Shader'], node_add_shader3.inputs[0])
        # Conectar Add Shader1 a Add Shader3
        links.new(node_add_shader2.outputs['Shader'], node_add_shader3.inputs[1])
        # Conectar Add Shader6 a Add Shader5
        links.new(node_add_shader6.outputs['Shader'], node_add_shader5.inputs[0])
        # Conectar Add Shader5 a Add Shader4
        links.new(node_add_shader5.outputs['Shader'], node_add_shader4.inputs[1])
        # Conectar Add Shader3 a Add Shader4
        links.new(node_add_shader3.outputs['Shader'], node_add_shader4.inputs[0])
        # Conectar Add Shader4 a Material Output
        links.new(node_add_shader4.outputs['Shader'], node_material_output.inputs[0])

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

        # Asegurarse de que el objeto esté en modo de objeto
        bpy.ops.object.mode_set(mode='OBJECT')
        
        # Establecer el objeto activo
        obj = bpy.context.scene.objects.get("velo_chopper_template")
        if obj is None:
            self.report({'ERROR'}, "No se encontró el objeto 'velo_chopper_template'.")
            return {'CANCELLED'}
        
        bpy.context.view_layer.objects.active = obj
        
        # Seleccionar el objeto
        bpy.ops.object.select_all(action='DESELECT')
        obj.select_set(True)

        # Crear una nueva imagen para el bake
        bake_image = bpy.data.images.new(name="template013", width=195, height=128, alpha=True)

        # Asignar la imagen a un nodo de textura de imagen en el material
        material = obj.material_slots[0].material
        nodes = material.node_tree.nodes
        texture_node = nodes.new(type='ShaderNodeTexImage')
        texture_node.image = bake_image
        material.node_tree.nodes.active = texture_node

        # Realizar el horneado
        bpy.ops.object.bake(type='COMBINED')

        # Guardar la imagen horneada con un nombre específico
        export_directory = context.scene.export_folder
        if not export_directory:
            self.report({'ERROR'}, "Debes seleccionar una carpeta de exportación.")
            return {'CANCELLED'}

        bake_image.filepath_raw = os.path.join(export_directory, "template013.png")
        bake_image.file_format = 'PNG'
        bake_image.save()

        self.report({'INFO'}, f"¡Textura horneada y guardada en {bake_image.filepath_raw}!")

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
                # Eliminar la extensión si ya existe
                filename, ext = os.path.splitext(img.name)
                if ext.lower() == ".png":
                    img.filepath_raw = os.path.join(export_directory, img.name)
                else:
                    img.filepath_raw = os.path.join(export_directory, f"{img.name}.png")
                img.file_format = 'PNG'
                img.save()

        self.report({'INFO'}, f"¡Se han exportado las texturas correctamente a {export_directory}!")

        return {'FINISHED'}

class CustomPanel(bpy.types.Panel):
    """Panel personalizado para configurar el template"""
    bl_label = "Texture Options"
    bl_idname = "PT_CustomPanel"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'velo_chopper_edit'

    def draw(self, context):
        layout = self.layout
        scene = context.scene

        layout.label(text="Export Folder:")
        layout.prop(scene, "export_folder", text="")
        layout.operator("wm.select_export_folder", text="Select", icon='FILE_FOLDER')

        layout.operator("wm.import_template", text="Import Template")
        layout.operator("wm.bake_textures", text="Bake Textures")
        layout.operator("wm.export_textures", text="Export Textures")

def register():
    bpy.utils.register_class(ImportTemplateOperator)
    bpy.utils.register_class(BakeTexturesOperator)
    bpy.utils.register_class(SelectExportFolderOperator)
    bpy.utils.register_class(ExportTexturesOperator)
    bpy.utils.register_class(CustomPanel)

    bpy.types.Scene.export_folder = bpy.props.StringProperty(name="Export Folder", subtype='DIR_PATH')

def unregister():
    bpy.utils.unregister_class(ImportTemplateOperator)
    bpy.utils.unregister_class(BakeTexturesOperator)
    bpy.utils.unregister_class(SelectExportFolderOperator)
    bpy.utils.unregister_class(ExportTexturesOperator)
    bpy.utils.unregister_class(CustomPanel)
    del bpy.types.Scene.export_folder

if __name__ == "__main__":
    register()
