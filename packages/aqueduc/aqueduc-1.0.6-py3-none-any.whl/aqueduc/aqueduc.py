import sys 
import os.path
import os 
import json 
import shutil
import datetime
import time
from typing import Dict,Any


def run():

    if not valid_parameter() :
        print("Wrong input. Input should be in form : SaveProgram PlanPath")
        sys.exit(1) 

    plan_path = sys.argv[1]
    
    if not(os.path.exists(plan_path)) or not(os.path.isfile(plan_path)):
        print("Wrong input. Invalid Plan File")
        sys.exit(1) 

    with open(plan_path) as plan_file: 
        
        plan = json.load(plan_file)
        target_path = plan["target"]

        if not(os.path.exists(target_path)) or not(os.path.isdir(target_path)):
            print("Error in Plan File. Invalid target")
            sys.exit(1) 

        for source in plan["sources"]:

            if not(os.path.exists(source["path"])) and not(os.path.isfile(source["path"])):
                print("Error in Plan File. Invalid source")
                sys.exit(1) 

            if source["options"]["removeExisting"]:
                try_remove_existing(source["path"],target_path)

            isFile = os.path.isfile(source["path"])
            limit = len(source["path"].split(os.path.sep)) -1 
            move(source["path"],source["options"],target_path,limit)

            if source["options"]["move"] and not isFile : 
                shutil.rmtree(source["path"]) 


def move(path: str, options: Dict[str,Any], target_path: str, depth : int) : 

    if os.path.isfile(path) : 

        if extension_forbidden(path,options): 
            print("forbidden extension")
            sys.exit(1) 

        if file_toolarge(path,options):
            print("too large")
            sys.exit(1) 

        if file_not_modified_since_date(path,options):
            print("No modification since date")
            sys.exit(1) 

        cut_path_list = [ el for i,el in enumerate(path.split(os.path.sep)) if i >= depth ]

        if not options["overwrite"] : 
            
            cut_path = os.path.sep.join(cut_path_list)
            if os.path.exists(target_path + os.path.sep + cut_path):
                print("Overwrite prevented")
                sys.exit(0) 
              
        # get the folder path of the final 
        final_target_path = target_path + os.path.sep + os.path.sep.join(cut_path_list)
        final_target_path_list = [el for el in final_target_path.split(os.path.sep)] 
        final_target_path_list.pop(-1)
        folder_path = os.path.sep.join(final_target_path_list)
  
        if not os.path.exists(folder_path) :
            os.makedirs(folder_path)
        
        if options["move"] : 
            shutil.move(path,final_target_path)
        else :
            shutil.copy(path,final_target_path)
        
    elif os.path.isdir(path) :

        if os.path.isfile(target_path):
            print("Cannot move folder in a file")
            return

        entries = [path + os.path.sep + x for x in os.listdir(path)]

        for entry in entries : 
            move(entry,options,target_path,depth)


def valid_parameter() -> bool:
    """ Check console argument validity 

    Returns:
        bool: True if there is only one argument, False otherwise 
    """
    return len(sys.argv) != 1


def extension_forbidden(path: str, options: Dict[str,Any]) -> bool: 

    extension = path.split(".")[-1]
    return extension in options["forbidden_extensions"] 


def file_toolarge(path: str, options: Dict[str,Any]) -> bool: 

    file_size = os.path.getsize(path)
    return options["size_limit"] != -1 and file_size >= options["size_limit"]


def file_not_modified_since_date(path: str, options: Dict[str,Any]) -> bool: 

    sec_since_epoch_param = None 

    try : 
        sec_since_epoch_param = datetime.datetime.strptime(options["last_date_allowed"], "%d %m %Y %H").timestamp() 
    except ValueError : 
        sys.exit("Invalid last_date_allowed option in parameter file") 
    
    sec_since_epoch_file = os.path.getmtime(path)

    return sec_since_epoch_file < sec_since_epoch_param

def try_remove_existing(path: str, target: str) -> bool:
    if os.path.isfile(target):
        os.remove(target)
        return True
    elif os.path.isdir(path) and os.path.isdir(target):
        final_path = target + os.path.sep + path.split(os.path.sep).pop()
        if(os.path.isdir(final_path)):
            shutil.rmtree(final_path)
            return True
    return False