import os
import re
import subprocess


def is_docker() -> bool:
    with open('/proc/self/cgroup', 'r') as procfile:
        result = subprocess.run(["grep", "container"], stdin=procfile, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        if result.returncode == 0:
            return True
        else:
            return False

    return False

def find_repository_name(start_dir="."):
    current_dir = os.path.abspath(start_dir)

    while current_dir != '/':  # Stop searching at the root directory
        for root, dirs, files in os.walk(current_dir):
            paths = [path for path in files if re.search("Snakefile|snakefile", path)]
            if paths:
                if is_docker == "TRUE":  # If the Snakefile is run inside a Docker container, then there will be only one Snakefile, and therefore we can automatically identify it
                    return re.sub("/workflow/|\.", "", os.path.relpath(root, start_dir))
                else:  # If the Snakefile is not running inside a Docker container, then get the relative path of the Snakefile from pwd
                    return re.sub("/workflow/|\.", "", os.path.join(root, start_dir) )

        current_dir = os.path.dirname(current_dir)

    # Of course, if a different path is provided with the --snakefile argument, this will be used by Snakemake
    return None  # Return None if no Snakefile or snakefile is found

def find_workflow_path(dir="."):
    home_directory = os.path.expanduser("~")
    repository_name = find_repository_name(dir)
    result = subprocess.run(["find", home_directory, "-type", "d", "-name", repository_name], capture_output=True, text=True)
    return result.stdout
