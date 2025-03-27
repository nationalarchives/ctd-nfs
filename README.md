# ctd-nfs
Code developed to support the National Farm Survey QA and transformation process. This includes libraries for combining string variants.

The repo contains the following files:
* The main library is nfs_document_checks.py. This file contains the code to read in the CSVs from the processing folder, processes the data and save the results into a new spreadsheet in the outputs folder 
* The above is supported by the data normalisation library (data_normalisation.py) which has the methods to support the string integration. 
 
## Anaconda

These instructions assume you have [Anaconda](https://www.anaconda.com/products/distribution) installed.

The relevant packages can be installed using pip install, if Anaconda is not available.

## Creating the nfs Anaconda environment

[General docs on managing environments](https://conda.io/projects/conda/en/latest/user-guide/tasks/manage-environments.html)

To create the conda environment for the first time, run the following three commands in Command Prompt or in Anaconda Powershell :

    conda create -n nfs python openpyxl rapidfuzz pyinstaller
    conda activate ape

The following instructions assume the nfs environment has been activated.

Optional - the environment can be kept up to date in future using:

    conda activate nfs
    conda update --all

If you are using MS Code to edit or run the APE code, you should associate the ape environment with the workspace. How to [Assign the ape conda environment to the workspace in MS VS Code](https://code.visualstudio.com/docs/python/environments)

## Building the application for distribution

Change directory to the directory containing the python files.

if using anaconda activate the nfs environment if not already activated (if activated, ignore the first line).

    conda activate nfs
    pyinstaller --name NFS_QA --hidden-import openpyxl.cell._writer nfs_document_checks.py

 Pyinstaller will generate a NFS_QA folder and put it in a dist folder. This will contain and executable file and a folder called _internal. The following folders need to be added to the NFS_QA folder - a process folder which contains an output folder (and optionally an ignore folder) as the processing and output folder are expected by the code. Once these folders have been added the NFS_QA folder can be shared (recommend zipping to distribute). 

 ## Running the code

If running the application then double clicking on the exe file will run the default process on any CSV files in the processing folder. The output will be saved to the output folder as xlsx files with the same name as the corresponding csv file. 
