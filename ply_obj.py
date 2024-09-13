import os
import argparse
import trimesh

# Function to convert PLY to OBJ
def convert_ply_to_obj(input_file, output_file):
    mesh = trimesh.load(input_file)
    mesh.export(output_file)
    print(f"Converted {input_file} to {output_file}")

# Function to convert OBJ to PLY
def convert_obj_to_ply(input_file, output_file):
    mesh = trimesh.load(input_file)
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

# Main function to handle argument parsing and conversions
def main():
    # Argument parser
    parser = argparse.ArgumentParser(description="Convert between .ply and .obj file formats.")
    parser.add_argument('--to_obj', action='store_true', help='Convert .ply files to .obj')
    parser.add_argument('--to_ply', action='store_true', help='Convert .obj files to .ply')
    parser.add_argument('--folder', type=str, required=True, help='Folder containing the files to convert')
    parser.add_argument('--delete_ours', action='store_true', help='Delete files containing "ours" in their filenames')
    
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
                convert_ply_to_obj(input_file, output_file)
    elif args.to_ply:
        for file in files:
            if file.endswith('.obj'):
                input_file = os.path.join(args.folder, file)
                output_file = os.path.join(args.folder, file.replace('.obj', '.ply'))
                convert_obj_to_ply(input_file, output_file)
    elif not args.delete_ours:
        print("Please specify either --to_obj, --to_ply, or --delete_ours.")

if __name__ == '__main__':
    main()