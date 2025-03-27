# ctd-nfs
Code developed to support the National Farm Survey QA and transformation process. This includes libraries for combining string variants.
 
## Anaconda

These instructions assume you have [Anaconda](https://www.anaconda.com/products/distribution) installed.

The relevant packages can be installed using pip install, if Anaconda is not available.

## Creating the nfs Anaconda environment

[General docs on managing environments](https://conda.io/projects/conda/en/latest/user-guide/tasks/manage-environments.html)

To create the conda environment for the first time, run the following three commands in Command Prompt or in Anaconda Powershell :

    conda create -n nfs python openpyxl rapidfuzz
    
    conda activate ape

The following instructions assume the nfs environment has been activated.

Optional - the environment can be kept up to date in future using:

    conda activate nfs
    conda update --all

If you are using MS Code to edit or run the APE code, you should associate the ape environment with the workspace. How to [Assign the ape conda environment to the workspace in MS VS Code](https://code.visualstudio.com/docs/python/environments)
