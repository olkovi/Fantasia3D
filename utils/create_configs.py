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
os.makedirs("configs_appearance", exist_ok=True)

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

appearance_config = {
    "mode": "appearance_modeling",
    "base_mesh": "out/sandcastle/dmtet_mesh/mesh.obj",
    "random_textures": "true",
    "iter": 2000,
    "coarse_iter": 300,
    "save_interval": 100,
    "texture_res": [ 2048, 2048 ],
    "train_res": [512, 512],
    "batch": 12,
    "kd_min" : [0.03, 0.03, 0.03],
    "kd_max" : [0.97, 0.97, 0.97],
    "ks_min" : [0, 0.08, 0],
    "ks_max" : [0, 0.9, 0],
    "display": [{"latlong" : "true"}, {"bsdf" : "kd"}, {"bsdf" : "ks"}, {"bsdf" : "normal"}],
    "envmap": "data/irrmaps/mud_road_puresky_4k.hdr",
    "env_scale" : 2.0,
    "train_background": "black",
    "validate" : "true",
    "out_dir": "sandcastle_appearance3",
    "text" : "A highly detailed sandcastle",
    "seed" : 42,
    "add_directional_text": "true",
    "camera_random_jitter": 0.3,
    "fovy_range": [25.71, 45],
    "elevation_range": [-10, 45],
    "guidance_weight": 50,
    "sds_weight_strategy": 2,
    "early_time_step_range": [0.02, 0.98],
    "late_time_step_range": [0.02, 0.98]
}


preprompt = "full frame, 3d model "
outfold = os.path.join("out","negtest_" + "\'"+preprompt+"\'").replace(":","_")
#os.makedirs(outfold, exist_ok=True)

word_list=[]
import copy
for orig1_prompt, orig2_prompt in prompt_pairs:
    split1 = orig1_prompt.split()
    split2 = orig2_prompt.split()
    configs = []
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
    configs.append(copy.deepcopy(chair_config))
    with open(os.path.join("configs_orig1", orig1_filename), "w") as f:
        json.dump(chair_config, f, indent=4)  # Write base config

    chair_config["text"] = preprompt + orig2_prompt
    chair_config["out_dir"] = os.path.join(outfold, firstword2)
    configs.append(copy.deepcopy(chair_config))
    with open(os.path.join("configs_orig2", orig2_filename), "w") as f:
        json.dump(chair_config, f, indent=4)  # Write edit config


    chair_config["text"] = preprompt + orig2_prompt
    chair_config["out_dir"] = os.path.join(outfold, firstword2) +"_edit"
    chair_config["sdf_init_shape"] ="custom_mesh"
    chair_config["base_mesh"]=os.path.join("out",firstword1,"dmtet_mesh","mesh.obj").replace("\\","/")
    configs.append(copy.deepcopy(chair_config))
    with open(os.path.join("configs_edit2", edit2_filename), "w") as f:
        json.dump(chair_config, f, indent=4)  # Write edit config

    chair_config["text"] = preprompt + orig1_prompt
    chair_config["out_dir"] = os.path.join(outfold, firstword1) +"_edit"
    chair_config["sdf_init_shape"] ="custom_mesh"
    chair_config["base_mesh"]=os.path.join("out",firstword2,"dmtet_mesh","mesh.obj").replace("\\","/")
    configs.append(copy.deepcopy(chair_config))
    with open(os.path.join("configs_edit1", edit1_filename), "w") as f:
        json.dump(chair_config, f, indent=4)  # Write edit config

    chair_config["sdf_init_shape"] = "ellipsoid"
    del chair_config["base_mesh"]
    print(len(configs))
    for config in configs:
        appearance_config["text"] = config["text"]
        appearance_config["base_mesh"] = os.path.join(config["out_dir"], "dmtet_mesh","mesh.obj").replace("\\","/")
        appearance_config["out_dir"] = config["out_dir"] + "_appearance"
        filename = appearance_config["out_dir"].split("\\")[-1] + ".json"
        print(filename)
        with open(os.path.join("configs_appearance", filename), "w") as f:
            json.dump(appearance_config, f, indent=4)  # Write edited appearance config

print(chair_config["out_dir"])
print("Configuration files created successfully!")
