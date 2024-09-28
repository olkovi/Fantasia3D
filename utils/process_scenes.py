import os
import argparse
import trimesh
import numpy as np
import shutil

def convert_ply_to_obj(input_file, output_file, inverse=False, scale_factor=None):
    mesh = trimesh.load(input_file)
    mesh = apply_rotation_and_translation(mesh, inverse, scale_factor)
    mesh.export(output_file)
    print(f"Converted {input_file} to {output_file}")

def convert_obj_to_ply(input_file, output_file, inverse=False, scale_factor=None):
    mesh = trimesh.load(input_file)
    mesh = apply_rotation_and_translation(mesh, inverse, scale_factor)
    mesh.export(output_file)
    print(f"Converted {input_file} to {output_file}")


def apply_rotation_and_translation(mesh, inverse=False, scale_factor=1):
    # rotate the mesh by 90 degrees around the Y-axis
    rotation_angle = np.radians(90)  # Rotate 90 degrees
    rotation_matrix1 = trimesh.transformations.rotation_matrix(rotation_angle, [-1, 0, 0])  # X-axis rotation
    rotation_matrix2 = trimesh.transformations.rotation_matrix(rotation_angle, [0, -1, 0])  # Y-axis rotation

    # Translate the mesh along the Y-axis
    translation_matrix = trimesh.transformations.translation_matrix([0, 0, -0.3])  # Adjust Y-axis
    scale_factor = 0.5#1/1.44 #0.6/2.4
    # scale the mesh
    scaling_matrix = trimesh.transformations.scale_matrix(scale_factor, [0, 0, 0])  # Scaling from origin

    # combine transformations: X rotation, Y rotation, translation, scaling
    transformation_matrix = rotation_matrix2 @ rotation_matrix1 @ scaling_matrix @ translation_matrix # 
    inverse_matrix = np.linalg.inv(transformation_matrix)

    if not inverse:
        mesh.apply_transform(transformation_matrix)
    else:
        mesh.apply_transform(inverse_matrix)

    return mesh

def process_scene(scene_folder, scale_factor=None, inverse=False):
    # Locate mesh file
    input_file = os.path.join(scene_folder, 'dmtet_mesh', 'mesh.obj')
    if not os.path.exists(input_file):
        print(f"Mesh file not found: {input_file}")
        return

    # Load and process the mesh
    mesh = trimesh.load(input_file)
    mesh = apply_rotation_and_translation(mesh, inverse, scale_factor)

    # output directory: /editing/<scene>/fantasia3d.transform/mesh/
    scene_name = os.path.basename(scene_folder)
    output_folder = os.path.join('./editing', scene_name, 'fantasia3d.transform', 'mesh')
    os.makedirs(output_folder, exist_ok=True)

    # save processed
    output_file = os.path.join(output_folder, 'mesh.obj')
    mesh.export(output_file)
    print(f"Saved processed mesh to {output_file}")

    # move to fantasia3d
    validate_folder = os.path.join(scene_folder, 'validate')
    if os.path.exists(validate_folder):
        for item in os.listdir(validate_folder):
            src = os.path.join(validate_folder, item)
            dest = os.path.join(output_folder, '..', item)  # Parent folder of mesh
            if os.path.isdir(src):
                shutil.move(src, dest)
            elif os.path.isfile(src):
                shutil.move(src, dest)

# Main function to handle argument parsing and conversions
def main():
    # Argument parser
    parser = argparse.ArgumentParser(description="Process and convert meshes between .ply and .obj formats, with optional scaling and reorienting.")
    parser.add_argument('--to_obj', action='store_true', help='Convert .ply files to .obj')
    parser.add_argument('--to_ply', action='store_true', help='Convert .obj files to .ply')
    parser.add_argument('--folder', type=str, required=True, help='Folder containing the files to convert')
    parser.add_argument('--inverse', action='store_true', help='Apply inverse rotation and translation')
    parser.add_argument('--scale', type=float, default=1.0, help='Scale factor for the mesh')

    args = parser.parse_args()

    # Ensure the folder exists
    if not os.path.isdir(args.folder):
        print(f"The folder {args.folder} does not exist.")
        return

    # Get list of files in the folder and process based on flags
    files = os.listdir(args.folder)

    for scene in files:
        scene_folder = os.path.join(args.folder, scene)
        if scene == "m1_11_horse_to_my_little_pony_meshedit_appearance":
            process_scene(scene_folder, scale_factor=args.scale, inverse=args.inverse)

if __name__ == '__main__':
    main()