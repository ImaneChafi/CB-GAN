import numpy as np
import h5py
import os
import open3d as o3d
import random

dataset_location = "/Users/adrianchang/documents/tree_dataset/acer"

filepath = os.path.join(dataset_location, "acer.h5")
f = h5py.File(filepath)
num = 2048
data = np.array(f['poisson_%d'%num][:])
print(data.shape)

sample = list(range(len(data)))
np.random.shuffle(sample)
for i in sample:
    xyz = np.array(data[i])
    pcd = o3d.geometry.PointCloud()
    pcd.points = o3d.utility.Vector3dVector(xyz)
    pcd.paint_uniform_color([0, 0, 0])
    o3d.visualization.draw_geometries([pcd])