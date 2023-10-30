import bpy
import os

scn = bpy.context.scene

for f in range(scn.frame_start, scn.frame_end + 1, scn.frame_step):
    scn.frame_set(f)
    mat = scn.camera.matrix_world
    print(mat)
