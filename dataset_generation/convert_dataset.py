import open3d as o3d
import numpy as np
import os
import h5py

# tree_types = [
# "lombardy_poplar",
# "acer",
# "palm",
# "silver_birch",
# "quaking_aspen",
# "cambridge_oak",
# "bamboo",
# "european_larch",
# "weeping_willow_o",
# "balsam_fir",
# "black_tupelo",
# "fan_palm",
# "sphere_tree",
# "black_oak",
# "hill_cherry",
# "sassafras",
# "douglas_fir",
# "apple",
# "small_pine",
# "weeping_willow"
# ]

tree_types = [
"acer"
]

#Number of trees per type to be generated 
N = 2000
dataset_location = "/Users/adrianchang/documents/tree_dataset/"

def generate_name(i):
    name = list(str(i))
    while not len(name) == 4:
        name.insert(0, '0')
    name = ''.join(name)
    return name

#Number of points to sample
num = 2048

total = np.zeros([N * len(tree_types), num, 3])
idx = 0
for type in tree_types:
    print(type)
    data = np.zeros([N, num, 3])
    for i in range(1, N + 1): 
        print(i, "/", N)
        name = generate_name(i)
        filepath = os.path.join(dataset_location, type, name + ".stl")
        mesh = o3d.io.read_triangle_mesh(filepath)
        mesh = mesh.sample_points_poisson_disk(num)
        mesh.scale(1 / np.max(mesh.get_max_bound() - mesh.get_min_bound()),
           center=mesh.get_center())
        xyz = np.asarray(mesh.points)
        data[i-1] = xyz
        total[idx] = xyz
        idx += 1
    print("Writing dataset")
    filepath = os.path.join(dataset_location, type, type + ".h5")
    hf = h5py.File(filepath, 'w')
    hf.create_dataset('poisson_%d'%num, data=data)
    hf.close()
    print("Done!")

# print("Writing dataset")
# filepath = os.path.join(dataset_location, "tree.h5")
# hf = h5py.File(filepath, 'w')
# hf.create_dataset('poisson_%d'%num, data=total)
# hf.close()
# print("Done!")
