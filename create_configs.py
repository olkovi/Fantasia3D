import json
import os

# --- 1. Load Prompt Pairs ---
with open("prompts_full.txt", "r") as f:
    prompt_pairs = [line.strip().split("&") for line in f]  # Read lines, split by comma

# --- 2. Folder Setup ---
os.makedirs("configs_orig1", exist_ok=True)
os.makedirs("configs_orig2", exist_ok=True)
os.makedirs("configs_edit1", exist_ok=True)
os.makedirs("configs_edit2", exist_ok=True)

# --- 3. Configuration Generation ---
chair_config = {
"mode": "geometry_modeling",
"sdf_init_shape": "ellipsoid",
"sdf_init_shape_scale": [0.6, 0.6, 0.6],
"translation_y": -0.3,
"random_textures": "true",
"iter": 4000,
"coarse_iter": 2000,
"save_interval": 100,
"train_res": [512, 512],
"batch": 16,
"dmtet_grid" : 256,
"display": [{"bsdf" : "normal"}],
"train_background": "black",
"validate" : "true",
"mesh_scale" : 2.4,
"out_dir": "antique_chair",
"text" : "antique wooden chair, no background",
"seed" : 42,
"add_directional_text": "false",
"camera_random_jitter": 0.4,
"fovy_range": [25.71, 45],
"elevation_range": [-10, 45],
"guidance_weight": 50
}  # Load chair.json into a Python dictionary

preprompt = "full frame, 3d model "
outfold = os.path.join("out","negtest_" + "\'"+preprompt+"\'").replace(":","_")
#os.makedirs(outfold, exist_ok=True)

word_list=[]

for orig1_prompt, orig2_prompt in prompt_pairs:
    split1 = orig1_prompt.split()
    split2 = orig2_prompt.split()
    if split1[0] not in word_list:
        firstword1 = split1[0]
        word_list.append(firstword1)
    else:
        firstword1 = split1[0] + " " + split1[1]
        word_list.append(firstword1)
    
    if split2[0] not in word_list:
        firstword2 = split2[0]
        word_list.append(firstword2)
    else:
        firstword2 = split2[0] + " " + split2[1]
        word_list.append(firstword2)
    
    orig1_filename = firstword1 + ".json"
    orig2_filename = firstword2 + ".json"
    edit1_filename = firstword1 + "_edit" + ".json"
    edit2_filename = firstword2 + "_edit" + ".json"

    # Modify chair_config['text'] for each pair
    chair_config["text"] = preprompt + orig1_prompt
    chair_config["out_dir"] = os.path.join(outfold, firstword1)
    with open(os.path.join("configs_orig1", orig1_filename), "w") as f:
        json.dump(chair_config, f, indent=4)  # Write base config

    chair_config["text"] = preprompt + orig2_prompt
    chair_config["out_dir"] = os.path.join(outfold, firstword2)
    with open(os.path.join("configs_orig2", orig2_filename), "w") as f:
        json.dump(chair_config, f, indent=4)  # Write edit config


    chair_config["text"] = preprompt + orig2_prompt
    chair_config["out_dir"] = os.path.join(outfold, firstword2) +"_edit"
    chair_config["sdf_init_shape"] ="custom_mesh"
    chair_config["base_mesh"]=os.path.join("out",firstword1,"dmtet_mesh","mesh.obj").replace("\\","/")
    with open(os.path.join("configs_edit2", edit2_filename), "w") as f:
        json.dump(chair_config, f, indent=4)  # Write edit config

    chair_config["text"] = preprompt + orig1_prompt
    chair_config["out_dir"] = os.path.join(outfold, firstword1) +"_edit"
    chair_config["sdf_init_shape"] ="custom_mesh"
    chair_config["base_mesh"]=os.path.join("out",firstword2,"dmtet_mesh","mesh.obj").replace("\\","/")
    with open(os.path.join("configs_edit1", edit1_filename), "w") as f:
        json.dump(chair_config, f, indent=4)  # Write edit config

    chair_config["sdf_init_shape"] = "ellipsoid"
    del chair_config["base_mesh"]
print(chair_config["out_dir"])
print("Configuration files created successfully!")
