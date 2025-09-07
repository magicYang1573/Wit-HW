
import io
import subprocess
from pathlib import Path
from dataclasses import dataclass, field
import os
import shutil
import hashlib


@dataclass
class RunConf:
    include_dir: Path = None
    timeout: float = None
    compile_timeout: float = None
    verbose: bool = False
    show_stdout: bool = False
    defines: list = field(default_factory=list)
    logfile: io.TextIOBase = None


def _conf_streams(conf: RunConf):
    if conf.logfile:
        return conf.logfile, conf.logfile
    stderr = None
    if conf.show_stdout:
        return None, stderr
    return subprocess.PIPE, stderr


# Verilator compile
def comp_with_verilator(working_dir: Path, files: list, conf: RunConf) -> bool:
    cmd_str = 'verilator -I. -f file_list.txt --cc -Wno-fatal --exe --build --binary -fno-table --coverage-line --trace --trace-structs'
    for name, value in conf.defines:
        cmd_str += f" +define+{name}={value} "
    for f_str in files:
        cmd_str += ' ' + f_str
    
    cmd_str += ' --top'
    cmd_str += ' testbench'
    cmd_str += ' > comp.log 2>&1'

    # print(cmd_str)
    
    stdout, stderr = _conf_streams(conf)
    
    try:
        r = subprocess.run(cmd_str, cwd=working_dir, check=False, stdout=stdout, stderr=stderr,
                           timeout=conf.compile_timeout, shell=True, executable='/bin/bash')
        # r = os.system(cmd_str)
        compiled_successfully = r.returncode == 0
        # print("Errorrrrrrr:", r.stderr.decode('utf-8'))
    except subprocess.TimeoutExpired:
        compiled_successfully = False
    
    return compiled_successfully


def sim_with_verilator(working_dir: Path, conf: RunConf) -> bool:
    cmd_str = './obj_dir/Vtestbench > sim.log'
    # print(cmd_str)
    stdout, stderr = _conf_streams(conf)
    try:
        # _print(conf, './simv')
        r = subprocess.run(cmd_str, cwd=working_dir, shell=True, executable='/bin/bash',
                            timeout=conf.timeout, stdout=stdout, stderr=stderr)
        success = r.returncode == 0
    except subprocess.TimeoutExpired:
        success = False  # failed
    return success




def file_md5(filepath):
    """Calculate the MD5 checksum of a file."""
    hash_md5 = hashlib.md5()
    with open(filepath, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()

def files_are_identical(src_file, dest_file):
    """Check if two files are identical by comparing their MD5 checksums."""
    if not os.path.exists(dest_file):
        return False
    return file_md5(src_file) == file_md5(dest_file)

''' 
if the file is the same with original running dir,
it will not cover the original files,
so it don't need compilation again when calling verilator
'''
def gen_basic_sim_env(verilator_running_dir, design, testbench, input_file):
    # Generate verilator running dir
    os.makedirs(verilator_running_dir, exist_ok=True)

    # Copy design and testbench files to running dir
    if len(design)!=0 and testbench!='':
        tmp_file_list_path = os.path.join(verilator_running_dir, 'file_list_tmp.txt')
        with open(tmp_file_list_path, 'w') as file_list:
            if isinstance(design, str):
                design_files = [design]
            elif isinstance(design, list):
                design_files = design
            else:
                design_files = []

            
            for file in design_files:
                file_name = file.split('/')[-1]
                dest_file = os.path.join(verilator_running_dir, file_name)
                if not files_are_identical(file, dest_file):
                    shutil.copy(file, dest_file)
                file_list.write(file_name + '\n')

            # Handle testbench
            if testbench != '':
                testbench_dest = os.path.join(verilator_running_dir, "testbench.sv")
                if not files_are_identical(testbench, testbench_dest):
                    shutil.copy(testbench, testbench_dest)
                file_list.write(testbench_dest.split('/')[-1] + "\n")

    # Handle input file
    if input_file != '':
        input_dest = os.path.join(verilator_running_dir, "workload.in")
        if not files_are_identical(input_file, input_dest):
            shutil.copy(input_file, input_dest)

    if not (len(design)==0 or testbench==''):
        file_list_path = os.path.join(verilator_running_dir, 'file_list.txt')
        if not files_are_identical(tmp_file_list_path, file_list_path):
            shutil.copy(tmp_file_list_path, file_list_path)
