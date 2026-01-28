import json
import bpy
import bmesh
import os
from . bex_utils import *

class BatEx_Export:

  def __init__(self, context):
    self.__context = context
    
    self.__export_folder = context.scene.batex_settings.export_folder
    if self.__export_folder.startswith("//"):
      self.__export_folder = os.path.abspath(bpy.path.abspath(context.scene.batex_settings.export_folder))

    self.__center_transform = context.scene.batex_settings.center_transform
    self.__apply_transform = context.scene.batex_settings.apply_transform
    self.__one_material_id = context.scene.batex_settings.one_material_ID
    self.__export_objects = context.selected_objects
    self.__export_animations = context.scene.batex_settings.export_animations
    self.__export_prefix = context.scene.batex_settings.export_prefix
    self.__unreal_mode = context.scene.batex_settings.unreal_mode
    self.__export_mode = context.scene.batex_settings.export_mode
    self.__export_smoothing = context.scene.batex_settings.export_smoothing
    self.__single_filename = context.scene.batex_settings.single_filename
    self.__use_prefix_single = context.scene.batex_settings.use_prefix_single
    self.__recent = context.scene.batex_settings.recent
    self.__mat_faces = {}
    self.__materials = []
  
  def do_center(self, obj):
    if self.__center_transform:
      loc = get_object_loc(obj)
      set_object_to_loc(obj, (0,0,0))
      return loc

    return None
  
  def recent_store(self, items):
    dic = {}
    dic['selection'] = []
    dic['export_folder'] = self.__export_folder
    dic['export_prefix'] = self.__export_prefix
    dic['export_animations'] = self.__export_animations
    dic['unreal_mode'] = self.__unreal_mode
    dic['export_smoothing'] = self.__export_smoothing
    dic['single_filename'] = self.__single_filename
    dic['use_prefix_single'] = self.__use_prefix_single
    dic['export_mode'] = self.__export_mode
    dic['center_transform'] = self.__center_transform
    dic['apply_transform'] = self.__apply_transform
    dic['one_material_ID'] = self.__one_material_id
    for item in items:
      dic['selection'].append(item.name)

    self.__context.scene.batex_settings.recent = json.dumps(dic).encode().decode()
    
    
  def recent_load_objects(self):
    recent = self.__recent
    if len(recent) > 0:
      dic = json.loads(recent.encode().decode())
      if 'selection' in dic and len(dic['selection']) > 0:
        objects = []
        for name in dic['selection']:
          if name in bpy.data.objects:
            objects.append(bpy.data.objects[name])
        return objects
    return []
  
  def recent_load_settings(self):
    recent = self.__recent
    if len(recent) > 0:
      dic = json.loads(recent.encode().decode())
      if 'export_folder' in dic:
        self.__export_folder = dic['export_folder']
      if 'export_prefix' in dic:
        self.__export_prefix = dic['export_prefix']
      if 'export_animations' in dic:
        self.__export_animations = dic['export_animations']
      if 'unreal_mode' in dic:
        self.__unreal_mode = dic['unreal_mode']
      if 'export_smoothing' in dic:
        self.__export_smoothing = dic['export_smoothing']
      if 'single_filename' in dic:
        self.__single_filename = dic['single_filename']
      if 'use_prefix_single' in dic:
        self.__use_prefix_single = dic['use_prefix_single']
      if 'export_mode' in dic:
        self.__export_mode = dic['export_mode']
      if 'center_transform' in dic:
        self.__center_transform = dic['center_transform']
      if 'apply_transform' in dic:
        self.__apply_transform = dic['apply_transform']
      if 'one_material_ID' in dic:
        self.__one_material_id = dic['one_material_ID']
  
  def export_recent(self):
    objects = self.recent_load_objects()
    # Warnings
    if len(objects) <= 0:
      raise Exception("No previous object selection available")
    
    self.recent_load_settings()
    
    selected_objects = bpy.context.selected_objects.copy()
    active_object = bpy.context.view_layer.objects.active
      
    self.__export_objects = objects
    bpy.ops.object.mode_set(mode='OBJECT')

    bpy.ops.object.select_all(action="DESELECT")
    for obj in objects:
      obj.select_set(state = True)
    
    bpy.context.view_layer.objects.active = objects[-1]
    self.do_export()
    bpy.ops.object.select_all(action='DESELECT')
    for obj in selected_objects:
      obj.select_set(state = True)
      
    bpy.context.view_layer.objects.active = active_object



  def remove_materials(self, obj):
    # Check if the object has mesh data and is not an armature
    if obj.type != 'MESH' or obj.data is None:
      return False

    mat_count = len(obj.data.materials)

    if mat_count > 1 and self.__one_material_id:
      # Save material ids for faces
      bpy.ops.object.mode_set(mode='EDIT')
      bm = bmesh.from_edit_mesh(obj.data)

      for face in bm.faces:
        self.__mat_faces[face.index] = face.material_index

      # Save and remove materials except the last one
      # so that we keep this as material id
      bpy.ops.object.mode_set(mode='OBJECT')
      self.__materials.clear()

      for idx in range(mat_count):
        self.__materials.append(obj.data.materials[0])
        if idx < mat_count - 1:
          obj.data.materials.pop(index=0)

      return True
    else:
      return False


  def restore_materials(self, obj):

    # Restore the materials for the object
    obj.data.materials.clear()

    for mat in self.__materials:
      obj.data.materials.append(mat)

    obj.data.update()

    # Reassign the material ids to the faces of the mesh
    bpy.ops.object.mode_set(mode='EDIT')

    bm = bmesh.from_edit_mesh(obj.data)

    for face in bm.faces:
        mat_index = self.__mat_faces[face.index]
        face.material_index = mat_index

    bmesh.update_edit_mesh(obj.data)

    bpy.ops.object.mode_set(mode='OBJECT')
    
  def fbx_export(self, name, types= {'MESH', 'EMPTY'}, use_prefix=True):
      
    # Export the selected object and its children as fbx
    bpy.ops.export_scene.fbx(
          check_existing=False,
          filepath=os.path.join(self.__export_folder, f"{self.__export_prefix if use_prefix else ''}{name}.fbx"),
          filter_glob="*.fbx",
          use_selection=True,
          object_types=types,
          bake_anim=self.__export_animations,
          bake_anim_use_all_bones=self.__export_animations,
          bake_anim_use_all_actions=self.__export_animations,
          use_armature_deform_only=True,
          use_mesh_modifiers=True,
          bake_space_transform=self.__apply_transform or self.__unreal_mode,
          mesh_smooth_type=self.__export_smoothing,
          add_leaf_bones=False,
          path_mode='ABSOLUTE',
          axis_forward='-Y' if self.__unreal_mode else '-Z',
          axis_up='Z' if self.__unreal_mode else 'Y',
          apply_scale_options='FBX_SCALE_NONE',
          apply_unit_scale=True,
          use_space_transform=True,
        )
    

  def do_export(self):

    bpy.ops.object.mode_set(mode='OBJECT')
    
    ex_object_types = {'MESH', 'EMPTY', 'OTHER'}
    
    recent_store = self.recent_store(self.__export_objects)

    if self.__export_animations:
      ex_object_types.add('ARMATURE')
    
    if self.__export_mode == 'BATCH':
      for obj in self.__export_objects:
        bpy.ops.object.select_all(action='DESELECT')
        obj.select_set(state=True)

        # Center selected object
        old_pos = self.do_center(obj)

        # Select children if exist
        for child in get_children(obj):
          child.select_set(state=True)

        # Remove materials except the last one
        materials_removed = self.remove_materials(obj)
        
        # Export the selected object and its children as fbx
        self.fbx_export(obj.name, types=ex_object_types, use_prefix=True)

        if materials_removed:
          self.restore_materials(obj)

        if old_pos is not None:
          set_object_to_loc(obj, old_pos)
    else:
      # Export the selected objects as fbx
      self.fbx_export(self.__single_filename, types=ex_object_types, use_prefix=self.__use_prefix_single)
