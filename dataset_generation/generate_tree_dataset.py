import bpy
import random
import os

# Full list
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

# Format per tree, all entries are tuples
# [leaf_count_range, branches_level_1, branches_level_2, branches_level_3, branches_level_4]
# If none, no changes
constraints = {
"lombardy_poplar": [(0,5), None ,(10,30), (5,20), None],
"acer": [(0,3), None ,(2,6), (3,5), (1,3)],
"palm": [(20,40), None ,(15,25), None, None],
"silver_birch": [(0,5), None ,(5,10), (5,10), None],
"quaking_aspen": [(5,5), None ,(10,15), (5,10), None],
"cambridge_oak": [(0,5), None ,(5,5), (1,1), (1,1)],
"bamboo": [(0,10), (15,25), (15,25), None, (10,10)],
"european_larch": [(0,5), None ,(10,20), (10,20), None],
"weeping_willow_o": [(0,5), None ,(2,3), (2,3), (10,20)],
"balsam_fir": [(0,5), None ,(15,20), (10,10), (2,2)],
"black_tupelo": [(0,5), None ,(15,25), (5,5), (5,5)],
"fan_palm": [(-45,-30), None ,(20,30), None, None],
"sphere_tree": [(0,15), None ,(30,60), (50,60), None],
"black_oak": [(0,15), None ,(15,25), (15,25), None],
"hill_cherry": [(0,5), None ,(15,25), (10,18), (10,15)],
"sassafras": [(5,10), None ,(10,15), (10,15), (10,15)],
"douglas_fir": [(20,40), None ,(50,75), (5,20), None],
"apple": [(0,15), None ,(10,20), (5,15), (2,5)],
"small_pine": [(50,100), None ,(40,70), None, None],
"weeping_willow": [(0,10), None ,(10,15), (15,20), (10,30)]
}

#Create directory if does not exist
if not os.path.exists(dataset_location):
    os.mkdir(dataset_location)

print("Clearing Screen")
bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete(use_global=False)

def randomize_params(type): #(Within reason)
    constraint = constraints[type]
    for i, restriction in enumerate(constraint):
        if restriction:
            if i == 0:
                choice = int(random.uniform(restriction[0], restriction[1]))
                bpy.context.scene.tree_leaf_blos_num_input = choice
            else:
                choice = int(random.uniform(restriction[0], restriction[1]))
                bpy.context.scene.tree_branches_input[i-1] = choice

def generate_name(i):
    name = list(str(i))
    while not len(name) == 4:
        name.insert(0, '0')
    name = ''.join(name)
    return name

for type in tree_types:
    print(type)
    #Load preset tree parameters 
    bpy.context.scene.custom_tree_load_params_input = "tree-gen.parametric.tree_params." + type
    bpy.ops.object.tree_gen_custom_load()
    
    subdir = os.path.join(dataset_location, type)
    if not os.path.exists(subdir):
        os.mkdir(subdir)
    
    for i in range(1, N + 1): 
        print(i, "/", N)
        randomize_params(type)
        #Generate Tree
        bpy.ops.object.tree_gen()
        bpy.ops.object.select_all(action='SELECT')

        #Export tree
        name = generate_name(i)
        filepath = os.path.join(subdir, name + ".stl")
        bpy.ops.export_mesh.stl(filepath=filepath, axis_forward="Z", axis_up="Y")

        #Delete tree for next iter
        bpy.ops.object.delete(use_global=False)

print("Done!")