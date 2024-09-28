import os
import argparse
import trimesh
import numpy as np

# Function to convert PLY to OBJ
def convert_ply_to_obj(input_file, output_file, rotate_and_reorient=False, scale_factor=None):
    mesh = trimesh.load(input_file)
    if rotate_and_reorient:
        mesh = apply_rotation_and_translation(mesh)
    if scale_factor:
        mesh = apply_scaling(mesh, scale_factor)
    mesh.export(output_file)
    print(f"Converted {input_file} to {output_file}")

# Function to convert OBJ to PLY
def convert_obj_to_ply(input_file, output_file, rotate_and_reorient=False, scale_factor=None):
    mesh = trimesh.load(input_file)
    if rotate_and_reorient:
        mesh = apply_rotation_and_translation(mesh)
    if scale_factor:
        mesh = apply_scaling(mesh, scale_factor)
    mesh.export(output_file)
    print(f"Converted {input_file} to {output_file}")

# Function to delete files containing 'ours' in their filename
def delete_files_with_ours(folder):
    files = os.listdir(folder)
    for file in files:
        if 'ours' in file:
            file_path = os.path.join(folder, file)
            os.remove(file_path)
            print(f"Deleted {file_path}")

# Function to apply rotation and translation to reorient the mesh
def apply_rotation_and_translation(mesh):
    # Step 1: Rotate the mesh by 90 degrees around the Y-axis
    rotation_angle = np.radians(90)  # Rotate 90 degrees
    rotation_matrix1 = trimesh.transformations.rotation_matrix(rotation_angle, [-1, 0, 0])
    rotation_matrix2 = trimesh.transformations.rotation_matrix(rotation_angle, [0, -1, 0])  # Y-axis
    rotation_matrix = rotation_matrix2@rotation_matrix1
    mesh.apply_transform(rotation_matrix) # X then Y-axis

    # Step 2: Optionally, translate the mesh along the Y-axis (adjust translation if needed)
    translation_matrix = trimesh.transformations.translation_matrix([0, 10, 0])  # Adjust Y-axis position if needed
    mesh.apply_transform(translation_matrix)

    return mesh

# Function to apply scaling to the mesh
def apply_scaling(mesh, scale_factor):
    # Create a scaling matrix
    scaling_matrix = trimesh.transformations.scale_matrix(scale_factor, [0, 0, 0])  # Uniform scaling from origin
    mesh.apply_transform(scaling_matrix)
    print(f"Scaled mesh by a factor of {scale_factor}")
    return mesh

# Main function to handle argument parsing and conversions
def main():
    # Argument parser
    parser = argparse.ArgumentParser(description="Convert between .ply and .obj file formats.")
    parser.add_argument('--to_obj', action='store_true', help='Convert .ply files to .obj')
    parser.add_argument('--to_ply', action='store_true', help='Convert .obj files to .ply')
    parser.add_argument('--folder', type=str, required=True, help='Folder containing the files to convert')
    parser.add_argument('--delete_ours', action='store_true', help='Delete files containing "ours" in their filenames')
    parser.add_argument('--rotate_and_reorient', action='store_true', help='Rotate and reorient the mesh during conversion')
    parser.add_argument('--scale', type=float, help='Scale the mesh by the given factor')

    args = parser.parse_args()

    # Ensure the folder exists
    if not os.path.isdir(args.folder):
        print(f"The folder {args.folder} does not exist.")
        return

    # Get list of files in the folder
    files = os.listdir(args.folder)

    # Handle deletion of files with 'ours' in their names
    if args.delete_ours:
        delete_files_with_ours(args.folder)

    # Convert based on the supplied flags
    if args.to_obj:
        for file in files:
            if file.endswith('.ply'):
                input_file = os.path.join(args.folder, file)
                output_file = os.path.join(args.folder, file.replace('.ply', '.obj'))
                convert_ply_to_obj(input_file, output_file, rotate_and_reorient=args.rotate_and_reorient, scale_factor=args.scale)
    elif args.to_ply:
        for file in files:
            if file.endswith('.obj'):
                input_file = os.path.join(args.folder, file)
                output_file = os.path.join(args.folder, file.replace('.obj', '.ply'))
                convert_obj_to_ply(input_file, output_file, rotate_and_reorient=args.rotate_and_reorient, scale_factor=args.scale)
    elif not args.delete_ours:
        print("Please specify either --to_obj, --to_ply, or --delete_ours.")

if __name__ == '__main__':
    main()
