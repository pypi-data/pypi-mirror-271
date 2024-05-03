from .nbtof_base import nbtof_base
from .nbtof_concat import nbtof_concat

import tempfile
import os
import re
import keyword
from typing import List
def isint(char :str):
    try:
        int(char)
        return True
    except:
        return False
def file_name_to_func_name(file_name: str):
    if keyword.iskeyword(file_name):
        return "_" + file_name
    if file_name.isidentifier():        
        return file_name

    return_str = ""
    for char in file_name:
        if (not char.isidentifier())*(not isint(char)):
            if char == "-":
                return_str = return_str + "_"
            elif char == " ":
                return_str = return_str + "_"
            elif char == ".":
                return_str = return_str + "_"
        else:
            return_str = return_str + char

    if isint(return_str[0]):
        return_str = "_" + return_str
    
    return return_str

def nbtof_generate(
    notebook_names:List[str],
    func_py_name:str,
    func_update:bool=True,
    ):
    """
    This function converts single or multiple notebook files into one .py file.
    This .py file has functions which perform the same processings with notebooks.
    
    Parameters
    ----------
    notebook_names : str or list
        notebooks are should be tagged.
    func_py_name : str
        output .py file with functions.
    
    Returns
    -------
    str
        The outputed .py file.
    """
    
    if func_py_name[-3:] != '.py':
        func_py_name = func_py_name +'.py'
    
    if type(notebook_names) == str:
        notebook_names = [notebook_names]
    
    for idx, notebook_name in enumerate(notebook_names):
        if notebook_name[-6:] != '.ipynb':
            notebook_name = notebook_name +'ipynb'
        if not os.path.isfile(notebook_name):
            raise FileNotFoundError(f"[Errno 2] No such file: {notebook_name}")     
        notebook_names[idx] = notebook_name
    
    with open(func_py_name, 'w') as f:
        pass
    
    with tempfile.TemporaryDirectory() as td:
        for _, notebook_name in enumerate(notebook_names):
            notebook_raw_name = os.path.splitext(os.path.basename(notebook_name))[0]
            notebook_func_name = file_name_to_func_name(notebook_raw_name)
            temp_func_file_path = td + '\\' + notebook_raw_name + ".py"
            _, _ = nbtof_base(
                notebook_name=notebook_name,
                func_name=notebook_func_name,
                func_file_name=temp_func_file_path,
                )
            nbtof_concat(
                func_py_name,
                temp_func_file_path,
                func_update = func_update)

    return func_py_name
