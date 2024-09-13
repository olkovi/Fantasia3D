import json
import os

# --- 1. Load Prompt Pairs ---
textfiles = []
for file in os.listdir("./data/meshediting_results_1"):
    if file.endswith(".txt"):
        textfiles.append(os.path.join("./data/meshediting_results_1", file))

meshfiles = []
for file in os.listdir("./data/meshediting_results_1"):
    if file.endswith(".obj"):
        meshfiles.append(os.path.join("./data/meshediting_results_1", file))

prompts = []
for textfile in textfiles:
    with open(textfile, "r") as f:
        lines = f.readlines()
        prompts.append(lines[1])
        #prompts.append = [line.strip().split("&") for line in f]  # Read lines, split by comma

# --- 2. Folder Setup ---
os.makedirs("configs_meshedit", exist_ok=True)


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
import copy
for orig1_prompt, filename, meshfile in zip(prompts, textfiles, meshfiles):

    split1 = orig1_prompt.split()
    configs = []
    if split1[0] not in word_list:
        firstword1 = split1[0]
        word_list.append(firstword1)
    else:
        firstword1 = split1[0] + " " + split1[1]
        word_list.append(firstword1)
    
    

    edit1_filename = firstword1 + "_meshedit" + ".json"

    chair_config["text"] = preprompt + orig1_prompt
    chair_config["out_dir"] = os.path.join(outfold, firstword1) +"_meshedit"
    chair_config["sdf_init_shape"] ="custom_mesh"
    chair_config["base_mesh"]=meshfile.replace("\\","/")
    configs.append(copy.deepcopy(chair_config))
    with open(os.path.join("configs_meshedit", edit1_filename), "w") as f:
        json.dump(chair_config, f, indent=4)  # Write edit config



print(chair_config["out_dir"])
print("Configuration files created successfully!")
