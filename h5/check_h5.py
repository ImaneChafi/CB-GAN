import numpy as np
import h5py
import os
import open3d as o3d
import random

dataset_location = "/Users/imanechafi/Desktop/PhD/SphericalHarmonics/h5"

filepath = os.path.join(dataset_location, "degree_1.h5") #change name based on the training category
f = h5py.File(filepath)
num = 3 #change this with the number of points in your meshes (or how much the model needs) 
data = np.array(f['poisson_%d'%num][:])
print(data.shape)

print(data)

## Uncomment this to visualize the data point clouds
# np.random.shuffle(sample)
# for i in sample:
#     xyz = np.array(data[i])
#     print(xyz)
#     pcd = o3d.geometry.PointCloud()
#     pcd.points = o3d.utility.Vector3dVector(xyz)
#     pcd.paint_uniform_color([0, 0, 0])
#     o3d.visualization.draw_geometries([pcd])
