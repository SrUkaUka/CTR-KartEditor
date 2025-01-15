import bpy
from bpy_extras.io_utils import ExportHelper
import os

class ImportHovercraftTemplateOperator(bpy.types.Operator):
    bl_idname = "import_scene.hovercraft_template"
    bl_label = "Import hovercraft template"
    bl_description = "Import the hovercraft_template.fbx file"
    
    def execute(self, context):
        fbx_path = r"C:\Users\Kevin\Desktop\Kevin\kart_editor\ctr-kart-editor\hovercraft_fbx"
        bpy.ops.import_scene.fbx(filepath=fbx_path)
        context.scene.show_edit_hovercraft = True
        self.report({'INFO'}, "Archivo FBX 'hovercraft_template.fbx' importado con éxito.")
        return {'FINISHED'}


class EditHovercraftOperator(bpy.types.Operator):
    bl_idname = "object.edit_hovercraft"
    bl_label = "Edit Hovercraft"
    bl_description = "Edit the imported hovercraft"
    
    def execute(self, context):
        obj_name = "hovercraft_color"
        
        if obj_name in bpy.data.objects:
            obj = bpy.data.objects[obj_name]
            
            if obj.active_material is not None:
                mat = obj.active_material
                nodes = mat.node_tree.nodes
                links = mat.node_tree.links
                
                # Eliminar los nodos específicos si existen
                for node_name in ["Principled BSDF", "Material Output", "Normal Map"]:
                    node_to_remove = [node for node in nodes if node.name == node_name]
                    for node in node_to_remove:
                        nodes.remove(node)
                
                mix_shader = None
                material_output = None
                color_attribute = None
                
                if 'Mix Shader' not in nodes:
                    mix_shader = nodes.new(type='ShaderNodeMixRGB')
                    mix_shader.location = (400, 0)
                    mix_shader.blend_type = 'MULTIPLY'
                    mix_shader.inputs['Fac'].default_value = 1.0
                else:
                    mix_shader = nodes['Mix Shader']
                
                if 'Material Output' not in nodes:
                    material_output = nodes.new(type='ShaderNodeOutputMaterial')
                    material_output.location = (600, 0)
                else:
                    material_output = nodes['Material Output']
                
                if 'Color Attribute' not in nodes:
                    color_attribute = nodes.new(type='ShaderNodeAttribute')
                    color_attribute.attribute_name = "Color"
                    color_attribute.location = (0, 0)
                else:
                    color_attribute = nodes['Color Attribute']
                
                # Conectar nodos existentes
                for node in nodes:
                    if node.type == 'TEX_IMAGE':
                        links.new(node.outputs['Color'], mix_shader.inputs['Color1'])
                
                if color_attribute:
                    links.new(color_attribute.outputs['Color'], mix_shader.inputs['Color2'])
                
                if mix_shader and material_output:
                    links.new(mix_shader.outputs['Color'], material_output.inputs['Surface'])
                
                self.report({'INFO'}, f"Nodos modificados en el objeto '{obj_name}'.")
            else:
                self.report({'WARNING'}, f"El objeto '{obj_name}' no tiene un material activo.")
        else:
            self.report({'WARNING'}, f"El objeto '{obj_name}' no se encuentra en la escena.")
        
        return {'FINISHED'}


class EditColorOperator(bpy.types.Operator):
    bl_idname = "object.edit_color"
    bl_label = "Edit Color"
    bl_description = "Edit vertex color of hovercraft_color object"
    
    def execute(self, context):
        obj_name = "hovercraft_color"
        
        if obj_name in bpy.data.objects:
            obj = bpy.data.objects[obj_name]
            
            bpy.context.view_layer.objects.active = obj
            bpy.ops.object.mode_set(mode='EDIT')
            
            bpy.ops.mesh.select_all(action='SELECT')
            
            bpy.ops.object.mode_set(mode='VERTEX_PAINT')
            
            self.report({'INFO'}, f"Objeto '{obj_name}' seleccionado en modo Edit y Vertex Paint.")
        else:
            self.report({'WARNING'}, f"El objeto '{obj_name}' no se encuentra en la escena.")
        
        return {'FINISHED'}


class ExportHovercraftOperator(bpy.types.Operator, ExportHelper):
    bl_idname = "export_scene.hovercraft"
    bl_label = "Export Hovercraft"
    bl_description = "Export the hovercraft and hovercraft_color objects to FBX"
    
    filename_ext = ".fbx"
    filter_glob: bpy.props.StringProperty(
        default="*.fbx",
        options={'HIDDEN'}
    )
    
    def execute(self, context):
        obj_names = ["hovercraft_color", "hovercraft"]
        
        if all(name in bpy.data.objects for name in obj_names):
            objs = [bpy.data.objects[name] for name in obj_names]
            
            bpy.ops.object.mode_set(mode='OBJECT')
            
            bpy.ops.object.select_all(action='DESELECT')
            for obj in objs:
                obj.select_set(True)
            
            bpy.context.view_layer.objects.active = objs[0]
            
            bpy.ops.object.join()
            
            bpy.ops.object.mode_set(mode='EDIT')
            bpy.ops.mesh.remove_doubles()
            bpy.ops.object.mode_set(mode='OBJECT')
            
            if objs[0].active_material is not None:
                mat = objs[0].active_material
                nodes = mat.node_tree.nodes
                links = mat.node_tree.links
                
                # Eliminar nodos específicos
                for node_name in ["ShaderNodeAttribute", "ShaderNodeMixRGB"]:
                    node_to_remove = [node for node in nodes if node.type == node_name]
                    for node in node_to_remove:
                        nodes.remove(node)
                
                # Crear y conectar el Principled BSDF
                principled_bsdf = nodes.new(type='ShaderNodeBsdfPrincipled')
                principled_bsdf.location = (400, 0)
                
                material_output = nodes.get('Material Output')
                
                if material_output:
                    links.new(principled_bsdf.outputs['BSDF'], material_output.inputs['Surface'])
                    
                for node in nodes:
                    if node.type == 'TEX_IMAGE':
                        links.new(node.outputs['Color'], principled_bsdf.inputs['Base Color'])
                
                self.report({'INFO'}, "Nodos modificados y Principled BSDF creado.")
            else:
                self.report({'WARNING'}, "El objeto no tiene un material activo.")
            
            export_path = self.filepath
            if not export_path:
                self.report({'ERROR'}, "No se ha especificado una ruta de exportación.")
                return {'CANCELLED'}
            
            bpy.ops.export_scene.fbx(
                filepath=export_path,
                use_selection=True,
                bake_anim=False,
                path_mode='COPY',
                embed_textures=False
            )
            
            self.report({'INFO'}, "Archivo FBX exportado con éxito.")
        else:
            self.report({'WARNING'}, "Uno o más objetos no se encuentran en la escena.")
        
        return {'FINISHED'}


class ImportHovercraftTemplatePanel(bpy.types.Panel):
    bl_label = "Hovercraft Import"
    bl_idname = "VIEW3D_PT_hovercraft_import"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'hovercraft_edit'
    
    def draw(self, context):
        layout = self.layout
        layout.operator("import_scene.hovercraft_template")
        
        if context.scene.show_edit_hovercraft:
            layout.operator("object.edit_hovercraft")
            layout.operator("object.edit_color")
            layout.operator("export_scene.hovercraft")


def register():
    bpy.utils.register_class(ImportHovercraftTemplateOperator)
    bpy.utils.register_class(EditHovercraftOperator)
    bpy.utils.register_class(EditColorOperator)
    bpy.utils.register_class(ExportHovercraftOperator)
    bpy.utils.register_class(ImportHovercraftTemplatePanel)
    bpy.types.Scene.show_edit_hovercraft = bpy.props.BoolProperty(
        name="Show Edit Hovercraft Button",
        description="Show the edit hovercraft button after importing",
        default=False
    )


def unregister():
    bpy.utils.unregister_class(ImportHovercraftTemplateOperator)
    bpy.utils.unregister_class(EditHovercraftOperator)
    bpy.utils.unregister_class(EditColorOperator)
    bpy.utils.unregister_class(ExportHovercraftOperator)
    bpy.utils.unregister_class(ImportHovercraftTemplatePanel)
    del bpy.types.Scene.show_edit_hovercraft


if __name__ == "__main__":
    register()
