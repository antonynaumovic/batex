from . bex_folder_op import *
from . bex_op import *
from . bex_panel import *
from bpy.props import *
from bpy.props import (
    BoolProperty,
    EnumProperty,
    FloatProperty,
    IntProperty,
    StringProperty,
)
import bpy
bl_info = {
    "name": "Batex",
    "author": "jayanam, Rodrigo Camacho (forked from jayanam), Antony Naumovic",
    "descrtion": "Batch export as Fbx",
    "blender": (5, 0, 0),
    "version": (0, 7, 0, 1),
    "location": "Batex panel",
    "warning": "",
    "category": "Import-Export"
}


class BatexSettings(bpy.types.PropertyGroup):
    export_folder: StringProperty(name="Export folder",
                                   subtype="DIR_PATH",
                                   description="Directory to export the fbx files into",
                                   options=set())

    export_prefix: StringProperty(name="Export prefix",
                                   default="SM_",
                                   description="Prefix to add to the exported fbx files",
                                   options=set())
    
    single_filename: StringProperty(name="Single filename",
                                   default="Objects",
                                   description="Filename to use when exporting a single file",
                                   options=set())
    
    use_prefix_single: BoolProperty(name="Use Prefix for Single Export",
                               default=True,
                               description="Use the export prefix when exporting a single file",
                                   options=set())

    center_transform: BoolProperty(name="Center transform",
                                    default=True,
                                    description="Set the pivot point of the object to the center",
                                   options=set())

    apply_transform: BoolProperty(name="Apply transform",
                                   default=True,
                                   description="Applies scale and transform (Experimental)",
                                   options=set())

    unreal_mode: BoolProperty(name="Unreal Mode",
                               default=True,
                               description="Applies setting for Unreal Engine exports (Y Forward, Z Up)",
                               options=set())
    
    export_mode: EnumProperty(
        name="Mode",
        description="Defines the export mode",
        items=(
            ('SINGLE', 'Single', 'Export all selected objects as a single fbx file', 0),
            ('BATCH', 'Batch', 'Export each selected object as a separate fbx file', 1),
        ),
        default='BATCH',
        options=set()
    )

    export_smoothing: EnumProperty(
        name="Smoothing",
        description="Defines the export smoothing information",
        items=(
            ('EDGE', 'Edge', 'Write edge smoothing', 0),
            ('FACE', 'Face', 'Write face smoothing', 1),
            ('OFF', 'Normals Only', 'Write normals only', 2),
            ('SMOOTH_GROUP', 'Smoothing Groups', 'Write face smoothing groups', 3),

        ),
        default='SMOOTH_GROUP',
        options=set()
    )

    export_animations: BoolProperty(name="Export Rig & Animations",
                                     default=False,
                                     description="Export rig and animations",
                                     options=set()
                                     )

    export_animations: BoolProperty(name="Export Rig & Animations",
                                     default=False,
                                     description="Export rig and animations",
                                     options=set()
                                     )

    one_material_ID: BoolProperty(name="One material ID",
                                   default=False,
                                   description="Export just one material per object",
                                   options=set()
                                   )
    recent: bpy.props.StringProperty (
		name="Recent export",
		default=""
	)


classes = (BATEX_PT_Panel, BATEX_PT_Panel_Batch, BATEX_PT_Panel_Single, BATEX_PT_Panel_Export,
           BATEX_OT_Operator, BATEX_OT_Operator_Recent, BATEX_OT_OpenFolder, BatexSettings)


def register():
    if bpy.context.preferences.experimental.use_extensions_debug:
        print("Registering Batex Add-on with Debugging")
    for cls in classes:
        bpy.utils.register_class(cls)
    bpy.types.Scene.batex_settings = bpy.props.PointerProperty(
        type=BatexSettings
    )
    


def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)
    del bpy.types.Scene.batex_settings


if __name__ == "__main__":
    register()
