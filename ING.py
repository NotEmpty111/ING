# I Need Gpu
import os
import sys
import time

Needed_GPU =[
    "titan_xp",
    "tesla"
]

def execCmd(cmd):
    r = os.popen(cmd)
    text = r.read()
    r.close()
    return text

def parse_gpu(text):
    gpu_list = {}
    text = text.split("\n")
    if len(text) == 4:
        return gpu_list

    for i,line in enumerate(text):
        line = line.strip()
        if i%2 == 0 or i==1:
            continue
        line = line.split(" ")
        line = [ i for i in line if i != "│" and i != "┆" and i != ""]
        if len(line) == 0:
            continue
        gpu_list[line[0]] = int(line[1])

    return gpu_list

def filter_gpu(gpu_list):
    new_gpu_list = {}
    for key in gpu_list:
        for gpu in Needed_GPU:
            # support prefix match
            if gpu in key:
                new_gpu_list[key] = gpu_list[key]
                break
    return new_gpu_list
        
def get_gpu_list():
    cmd = "scir-status"
    text = execCmd(cmd)
    gpu_list = parse_gpu(text)
    gpu_list = filter_gpu(gpu_list)
    gpu_list = sorted(gpu_list.items(),key = lambda item:item[1],reverse=True)
    print(gpu_list)
    return gpu_list

def change_script(script_dir,gpu):
    new_script_dir = script_dir.split(".sh")[0]+"_ING.sh"
    new_file = open(new_script_dir,"w")
    new_lines = []
    with open(script_dir,"r") as f:
        lines = f.readlines()
        for i,line in enumerate(lines):
            if "--gres" not in line:
                new_lines+=[line]
                continue
            gpu_cmd = f"#SBATCH --gres=gpu:{gpu}:1 \n"
            new_lines.append(gpu_cmd)
    for line in new_lines:
        new_file.write(line)
    new_file.close()
    return new_script_dir
    

def submit_task(sciript_dir):
    cmd = f"sbatch {sciript_dir}"
    return os.system(cmd)

if __name__ == "__main__":
    if len(sys.argv) == 1:
        print("Please specific the script name")
    script_dir = sys.argv[1]
    while(True):
        print("searching gpu.........")
        gpu_list = get_gpu_list()
        if len(gpu_list):
            break
        time.sleep(2)
    choosed_gpu = gpu_list[0][0]
    print("choose gpu:",choosed_gpu)
    new_script_dir = change_script(script_dir,choosed_gpu)
    print(new_script_dir)
    if not submit_task(new_script_dir):
        print("submit task sucessfully!! use gpu:",choosed_gpu,"the new scirpt is ",new_script_dir)
    else:
        print("sumit task failed")