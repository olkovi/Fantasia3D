
import os
import argparse

def getsceneid():
    parser = argparse.ArgumentParser(description="Scene Get from Index & Folder")

    parser.add_argument("--dataset", type=str, help="Dataset dir local path")
    parser.add_argument("--scene-id", type=int, help="Current config")
    args = parser.parse_args()

    configs = os.listdir(args.dataset)
    confdir = {}
    for index, config in enumerate(configs):
        confdir[index] = config
    return confdir[args.scene_id-1]

if __name__ == "__main__":
    print(getsceneid())
