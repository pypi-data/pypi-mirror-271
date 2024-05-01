# Aqueduc

Aqueduc is a small script used to move or copy files and folders using preconfigured parameters.\
It is usefull to automate recurring file transfers.

## Requirement

- Python 3 (tested with python 3.7.2)

## How to get

```console
git clone https://github.com/Mozenn/Aqueduc.git
```

## How to use

1. create a JSON configuration file following [Configuration-file](#Configuration-file) or by checking the example files in data/ folder

2. From the directory where the script file is located, run :

```console
python aqueduc.py RelativePath/To/ConfigFile
```

## Tips

### Configuration file

Configurations files are in JSON format following this structure:

- target (str): Path of the destination folder where source items will be moved to
- sources (array)
  - path (str): Path of the file or folder to move
  - options
    - overwrite (boolean): true to overwrite the file in target destination if it already exists
    - removeExisting (boolean): true to remove the file in target destination if it already exists
    - move (boolean): true to move, false to copy
    - size_limit (number): size limit in bytes. Files having a size above this limit will not be moved/copied to target
    - forbidden_extensions(array): file having one of the specified extension will not be moved/copied to target
    - last_date_allowed (str): file not modified since the specified date will not be moved/copied to target

### Other

- You can put the aqueduc.py file wherever you want and execute it from there, or add it to your PATH.
