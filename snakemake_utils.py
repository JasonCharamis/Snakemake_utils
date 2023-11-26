
import os, re, subprocess


## Automatically identify repository name based on the suggested structure for Snakemake directories
## You can learn more here(https://snakemake.readthedocs.io/en/stable/snakefiles/deployment.html)

def find_repository_name(start_dir="."):
    
    is_docker = os.environ.get("DOCKER_CONTAINER") == "TRUE"
    current_dir = os.path.abspath(start_dir)

    while current_dir != '/':  # Stop searching at the root directory
        for root, dirs, files in os.walk(current_dir):
            paths = [path for path in files if re.search("Snakefile|snakefile", path)]
            if paths:
               if is_docker == "TRUE": ## If the Snakefile is run inside a Docker container, then there will be only one Snakefile, and therefore we can automatically identify it
                  return re.sub("/workflow/","", os.path.relpath(root, start=start_dir) )
	       else: ##	If the Snakefile is not	running	inside a Docker container, then get the relative path of the Snakefile from pwd (assuoming that the 
               	  return os.path(root, start=start_dir)

        current_dir = os.path.dirname(current_dir)

        ## Of course, if a different path is provided with the --snakefile argument, this will be used by Snakemake
        
    return None     # Return None if no Snakefile or snakefile is found


## Find path of the workflow directory based on repository name, used for identifying the config.yaml file path
## Of course, if a new path is provided by --configfile argument, Snakemake will use that
def find_workflow_path():
  home_directory = os.path.expanduser("~")
  repository_name = find_repository_name(start_dir=".")
  result = subprocess.run(["find", home_directory, "-type", "d", "-name", repository_name ], capture_output=True, text=True)
  return result.stdout
