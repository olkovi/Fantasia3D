import json
import os

# --- 1. Load Prompt Pairs ---
textfiles = []
num = 1
mode = "meshedit_appearance"
path = "./data/meshediting_results_" +str(num)
os.makedirs("configs_meshedit", exist_ok=True)
os.makedirs("configs_meshedit_appearance", exist_ok=True)

for file in os.listdir(path):
    if file.endswith(".txt"):
        textfiles.append(os.path.join(path, file))

meshfiles = []
for file in os.listdir(path):
    if file.endswith(".obj"):
        meshfiles.append(os.path.join(path, file))
originals = []
prompts = []
origlist = []
for textfile in textfiles:
    with open(textfile, "r") as f:
        lines = f.readlines()
        orig = lines[0].split(" ")[0].replace(",","").replace("\n","")
        i = 0
        while orig in origlist:
            i+=1
            try:
                nextword = "_"+lines[0].split(" ")[i].replace(",","").replace("\n","")
                orig = orig + nextword
            except IndexError:
                pass
            finally:
                orig = orig + "_"+str(i)

        if orig not in origlist:
            originals.append(orig)
            origlist.append(orig)
        else:
            orig = orig + "_" + lines[0].split(" ")[1]
            originals.append(orig)
            origlist.append(orig)
        prompts.append(lines[1])
        #prompts.append = [line.strip().split("&") for line in f]  # Read lines, split by comma

# --- 2. Folder Setup ---
os.makedirs("configs_meshedit", exist_ok=True)


# --- 3. Configuration Generation ---
chair_config = {
"mode": "geometry_modeling",
"sdf_init_shape": "custom_mesh",
"sdf_init_shape_scale": [0.6, 0.6, 0.6],
"translation_y": -0.3,
"random_textures": "true",
"iter": 3000,
"coarse_iter": 300,
"save_interval": 100,
"train_res": [512, 512],
"batch": 10,
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
if mode == "meshedit":
    used_config = chair_config
elif mode == "meshedit_appearance":
    used_config = appearance_config

preprompt = "full frame, 3d model "
topfold = os.path.join("out",mode).replace("\\","/")

word_list=[]
import copy
for orig1_prompt, filename, original, meshfile in zip(prompts, textfiles, originals, meshfiles):

    split1 = orig1_prompt.split(",")
    configs = []
    if split1[0] not in word_list:
        firstword1 = split1[0].replace(' ','_')
        word_list.append(firstword1)
    else:
        firstword1 = (split1[0] + "" + split1[1]).replace(',','')
        word_list.append(firstword1)
    print("\n")
    print(meshfile)
    print(orig1_prompt)

    edit1_filename = ("m"+str(num)+"_"+meshfile[-10:-8]+"_"+original + "_to_" + firstword1 + "_"+ mode).replace(" ","_")
    print(edit1_filename)
    used_config["text"] = preprompt + orig1_prompt
    outfold = os.path.join(topfold, edit1_filename).replace("\\","/")
    used_config["out_dir"] = outfold #(os.path.join(topfold, firstword1) +"_meshedit").replace("\\","/")
    if mode == "meshedit": 
        used_config["base_mesh"] = meshfile.replace("\\","/")
    elif mode == "meshedit_appearance":
        used_config["base_mesh"] = os.path.join(outfold,"dmtet_mesh","mesh.obj").replace("\\","/").replace("meshedit_appearance","meshedit")
    configs.append(copy.deepcopy(used_config))
    with open(os.path.join("configs_"+mode, edit1_filename) + ".json", "w") as f:
        json.dump(used_config, f, indent=4)  # Write edit config



print(used_config["out_dir"])
print(used_config["base_mesh"])
print("Configuration files created successfully!")
