import trimesh,sys,numpy as np
for n in sys.argv[1:]:
    m=trimesh.load(f"cad/{n}.stl"); m.merge_vertices(digits_vertex=5)
    m.update_faces(m.nondegenerate_faces()); m.update_faces(m.unique_faces()); m.remove_unreferenced_vertices()
    trimesh.repair.fill_holes(m); trimesh.repair.fix_normals(m)
    m.export(f"cad/{n}.stl"); print(n,m.is_watertight,round(m.volume,1),len(m.faces))
