import open3d as o3d
import numpy as np
import os
import h5py

# Full list
tree_types = [""]
# Number of trees per type to be generated 
N = 78
dataset_location = "/Users/imanechafi/Desktop/PhD/MICCAI/prep"

def generate_name(i):
    name = list(str(i))
    while not len(name) == 4:
        name.insert(0, '0')
    name = ''.join(name)
    return name

# Number of points to sample
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
        center = mesh.get_center()
        mesh.translate(-center)
        xyz = np.asarray(mesh.points)
        data[i-1] = xyz
        total[idx] = xyz
        idx += 1

print("Writing dataset")
filepath = os.path.join(dataset_location, "priors.h5")
hf = h5py.File(filepath, 'w')
hf.create_dataset('poisson_%d'%num, data=total, compression="gzip", compression_opts=9)
hf.close()
print("Done!")
