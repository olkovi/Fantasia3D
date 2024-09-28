#!/bin/bash

# Set the path to the directory containing subdirectories
parent_dir="./meshedit"

# Loop through each subdirectory in the parent directory
for dir in "$parent_dir"/*/; do
  # Check if the mesh.obj file exists in the dmtet_mesh subdirectory
  if [ -f "$dir/dmtet_mesh/mesh.obj" ]; then
    echo "Found: $dir/dmtet_mesh/mesh.obj"
  else
    echo "Missing: $dir/dmtet_mesh/mesh.obj"
  fi
done