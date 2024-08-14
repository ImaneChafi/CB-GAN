import pyvista as pv
import numpy as np
import matplotlib.pyplot as plt
from scipy.spatial import cKDTree

## Code to generate preparations automatically using geometric methods
## Imane Chafi, 2024

# Load your meshes
initial_mesh = pv.read('/Users/imanechafi/Desktop/PhD/data/marginline_tests/Incisors/shells/6027-31.stl')
ground_truth_mesh = pv.read('/Users/imanechafi/Desktop/PhD/data/marginline_tests/Incisors/dies/6027-31.stl')

# Extract the bounds of the meshes
bounds = initial_mesh.bounds
min_z = bounds[4]  # Minimum Z value (bottom)
max_z = bounds[5]  # Maximum Z value (top)

# Define the base plane (0.05mm from the base)
base_plane_z = min_z + 0.05

# Define the new tip plane to be 3 mm from the original top (shorter tip)
new_tip_z = max_z - 3.0  # 3 mm from the top

# Define the start of the tapering effect
taper_start_z = min_z + 0.005  # Height above the base where tapering starts

# Define parameters for side shrinkage and tapering
side_shrink_factor = 12  # Small squeeze effect
taper_factor = 0.7  # Adjust this value for tapering effect

# Create a new mesh that will be the modified version
modified_mesh = initial_mesh.copy()

def apply_shrinkage_and_taper(mesh, base_z, taper_start_z, new_tip_z, side_shrink_factor, taper_factor):
    vertices = mesh.points
    new_vertices = vertices.copy()
    center_x, center_y = mesh.center[:2]

    for i in range(vertices.shape[0]):
        x, y, z = vertices[i]

        if z > base_z:
            # Scale the height proportionally to the new tip height
            height_fraction = (z - base_z) / (max_z - base_z)
            new_z = base_z + height_fraction * (new_tip_z - base_z)
            new_vertices[i, 2] = new_z

            # Apply side squeeze effect close to the base
            if z > base_z:
                radial_distance = np.sqrt((x - center_x) ** 2 + (y - center_y) ** 2)
                if z <= taper_start_z:
                    # Apply squeeze effect
                    new_radial_distance = radial_distance * (1 - side_shrink_factor)
                else:
                    # Apply taper effect
                    new_radial_distance = radial_distance * (1 - taper_factor * height_fraction)

                angle = np.arctan2(y - center_y, x - center_x)
                new_x = center_x + new_radial_distance * np.cos(angle)
                new_y = center_y + new_radial_distance * np.sin(angle)
                new_vertices[i, 0] = new_x
                new_vertices[i, 1] = new_y

    mesh.points = new_vertices
    return mesh

# Apply the shrinkage and taper function
modified_mesh = apply_shrinkage_and_taper(modified_mesh, base_plane_z, taper_start_z, new_tip_z, side_shrink_factor, taper_factor)

# Save and plot the modified mesh
modified_mesh.save('/Users/imanechafi/Desktop/PhD/data/marginline_tests/Incisors/prep_auto/shrunken_mesh.stl')
modified_mesh.plot()

# Compute the difference between the initial and modified meshes
def compute_difference(mesh1, mesh2):
    # Create KDTree for fast nearest neighbor search
    tree1 = cKDTree(mesh1.points)
    distances, _ = tree1.query(mesh2.points, k=1)
    return distances

# Compute distances for heatmap
distances = compute_difference(initial_mesh, modified_mesh)
heatmap = np.zeros(initial_mesh.points.shape[0])

# Fill the heatmap
for i in range(len(distances)):
    heatmap[i] = distances[i]

# Visualize the heatmap
p = pv.Plotter(shape=(1, 2))

# Plot initial vs. modified mesh
p.subplot(0, 0)
p.add_mesh(initial_mesh, color='white', opacity=0.5)
p.add_mesh(modified_mesh, color='red', opacity=0.5)
p.add_title('Initial vs Modified Mesh')

# Plot heatmap
heatmap_mesh = initial_mesh.copy()
heatmap_mesh.point_data['Heatmap'] = heatmap
p.subplot(0, 1)
p.add_mesh(heatmap_mesh, scalars='Heatmap', cmap='coolwarm')
p.add_title('Heatmap of Differences')

# Compare ground truth with the modified mesh
def compute_difference_with_ground_truth(mesh1, mesh2):
    # Create KDTree for fast nearest neighbor search
    tree1 = cKDTree(mesh1.points)
    distances, _ = tree1.query(mesh2.points, k=1)
    return distances

# Compute distances for ground truth comparison
gt_distances = compute_difference_with_ground_truth(ground_truth_mesh, modified_mesh)
gt_heatmap = np.zeros(ground_truth_mesh.points.shape[0])

# Fill the heatmap
for i in range(len(gt_distances)):
    gt_heatmap[i] = gt_distances[i]

# Plot heatmap for ground truth comparison
p = pv.Plotter(shape=(1, 2))

# Plot modified vs. ground truth mesh
p.subplot(0, 0)
p.add_mesh(ground_truth_mesh, color='white', opacity=0.5)
p.add_mesh(modified_mesh, color='blue', opacity=0.5)
p.add_title('Ground Truth vs Modified Mesh')

# Plot heatmap
gt_heatmap_mesh = ground_truth_mesh.copy()
gt_heatmap_mesh.point_data['Heatmap'] = gt_heatmap
p.subplot(0, 1)
p.add_mesh(gt_heatmap_mesh, scalars='Heatmap', cmap='coolwarm')
p.add_title('Heatmap of Ground Truth Differences')

p.show()
