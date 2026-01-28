import bpy
from bpy.types import Panel


class BATEX3DPanel:
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Batex"

    @classmethod
    def poll(cls, context):
        return context is not None


class BATEX_PT_Panel(BATEX3DPanel, Panel):
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_label = "Batex"
    bl_category = "Batex"

    bl_idname = "BATEX_PT_panel_main"

    def draw_header(self, context):
        self.layout.label(text="", icon="EXPORT")

    def draw(self, context):

        layout = self.layout
        scene = context.scene
        settings = scene.batex_settings

        row = layout.row()
        row.prop(settings, "export_mode", expand=True)

        row = layout.row()
        row.label(text="Export folder:")

        row = layout.row()
        col = row.column()
        col.prop(settings, "export_folder", text="")

        col = row.column()
        col.operator('object.bex_ot_openfolder', text='', icon='FILE_TICK')

        row = layout.row()
        row.prop(settings, "unreal_mode", text="Unreal Mode")

        row_smooth = layout.row()
        col_smooth_lbl = row_smooth.column()
        col_smooth_lbl.label(text="Smoothing:")

        row = layout.row()
        row.prop(settings, "export_prefix", text="Prefix")

        col_smooth = row_smooth.column()
        col_smooth.alignment = 'EXPAND'
        col_smooth.prop(settings, "export_smoothing", text="")
        row = layout.row()
        row.prop(settings, "export_animations")

class BATEX_PT_Panel_Batch(BATEX3DPanel, Panel):
    bl_parent_id = BATEX_PT_Panel.bl_idname
    bl_label = "Batch Export Settings"
    bl_idname = "BATEX_PT_panel_batch"
    
    @classmethod
    def poll(cls, context):
        return bpy.context.scene.batex_settings.export_mode == 'BATCH'
    
    def draw_header(self, context):
        self.layout.label(text="", icon="GROUP")

    def draw(self, context):

        layout = self.layout
        settings = context.scene.batex_settings
        layout.use_property_split = True
        layout.use_property_decorate = False
        col = layout.column()
        row = col.row()
        row.prop(settings, "center_transform", text="Center transform")

        row = col.row()
        row.prop(settings, "apply_transform", text="Apply transform")

        row = col.row()
        row.prop(settings, "one_material_ID", text="One material ID")
        
class BATEX_PT_Panel_Single(BATEX3DPanel, Panel):
    bl_parent_id = BATEX_PT_Panel.bl_idname
    bl_label = "Single Export Settings"
    bl_idname = "BATEX_PT_panel_single"
    
    @classmethod
    def poll(cls, context):
        return bpy.context.scene.batex_settings.export_mode == 'SINGLE'
    
    def draw_header(self, context):
        self.layout.label(text="", icon="OBJECT_DATA")

    def draw(self, context):
        layout = self.layout
        settings = context.scene.batex_settings
        layout.use_property_split = True
        layout.use_property_decorate = False
        col = layout.column()
        row = col.row()
        row.label(text="Export Filename:")
        row = col.row(align=True)
        row.column().prop(settings, "use_prefix_single", icon="NODE_SIDE", icon_only=True)
        row.column().prop(settings, "single_filename", text="")

class BATEX_PT_Panel_Export(BATEX3DPanel, Panel):
    bl_label = "Batex Export"
    bl_idname = "BATEX_PT_panel_export"

    def draw(self, context):

        layout = self.layout
        scene = context.scene
        row = layout.row(align=True)
        row.operator('object.bex_ot_operator', text='Export')
        if scene.batex_settings.recent != "":
            row.operator('object.bex_ot_operator_recent', text='', icon='RECOVER_LAST')
