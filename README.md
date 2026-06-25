# ctd-nfs
Code developed to support the National Farm Survey QA and transformation process. This includes libraries for combining string variants.

The repo contains the following files:
* The main library is nfs_document_checks.py. This file contains the code to read in the CSVs from the processing folder, processes the data and save the results into a new spreadsheet in the outputs folder 
* The above is supported by the data normalisation library (data_normalisation.py) which has the methods to support the string integration. 

NOTES:
Information Asset ID (IAID) is the unique identifier of the record. Replica ID (RID) is the unique identifier of the set of digital files associated with the record. 
For IAID, we discussed that whoever is transferring the data holds the source of truth of the IAIDs, i.e. they manage them, it is not Discovery that manages the IAIDs. 
e.g. for the Catalogue transfer process, the IAIDs are generated and managed through an EAV database; 
for the Parliamentary Archives records the IAIDs are an existing UUID field in Axiell, for DRI and TDR those systems generate and manage the IAIDs. 
So what I'm saying is, your system will have to generate and manage the IAIDs. 
By manage I mean, if a record changes, when it gets resent to Discovery it has to be with the same IAID 
otherwise Discovery would create a new record rather than update the existing. 

Replica ID (RID) is a bit easier as it doesn't have to be persistent. 
When a record is resent to Discovery we delete the existing and insert a new (with same IAID) so the RID could be different to the original sent.

Source depicts the type of record being sent. e.g. "PA" for Parliamentary Archives. 
Discovery uses this to identify the type of record and present it in whatever fashion required. For Farm Survey can you use "FS" please. 
Discovery needs this in order to know it has to deal with records at Cataloguing level 8 - SubItem. 
Title can be blank if no value exists for Farm Survey records. 
If there is no title the Discovery code takes the first 128 characters of the Scope Content and presents that as the Title. (Something like 128 chars.)

 

## Building the application for distribution

Change directory to the directory containing the python files.

if using anaconda activate the nfs environment if not already activated (if activated, ignore the first line).

    conda activate nfs
    pyinstaller --name NFS_QA --hidden-import openpyxl.cell._writer nfs_document_checks.py

 Pyinstaller will generate a NFS_QA folder and put it in a dist folder. This will contain and executable file and a folder called _internal. The following folders need to be added to the NFS_QA folder - a process folder which contains an output folder (and optionally an ignore folder) as the processing and output folder are expected by the code. Once these folders have been added the NFS_QA folder can be shared (recommend zipping to distribute). 

 ## Running the code

If running the application then double clicking on the exe file will run the default process on any CSV files in the processing folder. The output will be saved to the output folder as xlsx files with the same name as the corresponding csv file. 
