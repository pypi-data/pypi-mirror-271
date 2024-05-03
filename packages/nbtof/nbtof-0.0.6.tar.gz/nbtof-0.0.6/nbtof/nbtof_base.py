import tempfile
import os
import subprocess
import sys
import copy
import warnings

def nbtof_base(
    notebook_name,
    func_name=None,
    func_file_name=None,
    ):
    """
    This function converts noetbook into a function that performs the same processing as the notebook according to nbtof tags.
    
    Parameters
    ----------
    notebook_name : str
        notebook file path
    func_name : str
        function's name. If nothing is assigned, func_name gets notebook file name.
    func_file_name : str
        the .py file name that has the converted function.
    
    Returns
    -------
    tuple
        str
            output function file path.
        str
            output function file name.
    """
    
    if func_name is None:
        func_name = os.path.split(os.path.splitext(notebook_name)[0])[1]
        func_name = func_name.replace("-","_")
        
    if func_file_name is None:
        func_file_path = os.path.splitext(notebook_name)[0] + '.py'
    elif '.py' in func_file_name:
        func_file_path = func_file_name
    elif ".py" not in func_file_name:
        func_file_path = func_file_name + '.py'
    
    code_dict = {
        '#@header': -3,
        '# In[': -2,
        '#@ignore': -1,
        '#@advance': 0,
        '#@func': 1,
        '#@param': 2,
        '#@args': 3,
        '#@default': 4,
        '#@kwargs': 5,
        '#@help': 6,
        '#@plane': 7,
        '#@return': 8,
        '#@r_advance': 9,
    }
    
    table_hist_list = []
    with tempfile.TemporaryDirectory() as td:
        jupyter_path = "\"" + sys.base_prefix + '\\Scripts\\jupyter.exe' + "\""
        instant_py_file_path = td + '\\' + os.path.splitext(os.path.split(notebook_name)[1])[0] + '.py'
        nbconvert_cmd = jupyter_path + ' nbconvert ' + "\"" + notebook_name + "\"" + ' --to python --output '  + "\"" + instant_py_file_path + "\""
        
        returncode = subprocess.Popen(nbconvert_cmd, shell=True)
        _ = returncode.wait()
    
        with open(instant_py_file_path) as f:
            instant_table = []
            code_num = code_dict['#@header']
            for i, line in enumerate(f):
                if '#@ignore' == line[:len('#@ignore')]:
                    code_num = code_dict['#@ignore']
                elif '#@plane' in line[:len('#@plane')]:
                    code_num = code_dict['#@plane']
                elif '# In[' in line[:len('# In[')]:
                    code_num = code_dict['# In[']
                elif '#@advance' == line[:len('#@advance')]:
                    code_num = code_dict['#@advance']
                elif '#@param' == line[:len('#@param')]:
                    code_num = code_dict['#@param']
                elif '#@args' == line[:len('#@args')]:
                    code_num = code_dict['#@args']
                elif '#@default' == line[:len('#@default')]:
                    code_num = code_dict['#@default']
                elif '#@kwargs' == line[:len('#@kwargs')]:
                    code_num = code_dict['#@kwargs']
                elif '#@help' == line[:len('#@help')]:
                    code_num = code_dict['#@help']
                elif '#@return' == line[:len('#@return')]:
                    code_num = code_dict['#@return']
                elif '#@r_advance' == line[:len('#@r_advance')]:
                    code_num = code_dict['#@r_advance']
                    
                instant_table.append([code_num, line, i+1, ])
    
    instant_table = instant_table[:-1]
    table_hist_list.append(instant_table)
    
    # remove header
    instant_table = []
    for instant_list in table_hist_list[-1]:
        if (instant_list[0] != code_dict['#@header']):
            instant_table.append(instant_list)
    table_hist_list.append(instant_table)
    
    # remove -2, and adding plane
    instant_table = []
    check_num = -1
    for instant_list in table_hist_list[-1]:
        check_num = check_num - 1
        if (instant_list[0] == code_dict['# In['])*('# In[' == instant_list[1][:len('# In[')]):
            instant_table = instant_table[:len(instant_table)-2]
            check_num = 3
        
        if (check_num == 0)*(instant_list[0]==code_dict['# In[']):
            instant_table.append([code_dict['#@plane'], '\n', -1])
            instant_table.append([code_dict['#@plane'], '#@plane', -1])
    
        if check_num <= 0:
            if instant_list[0] == code_dict['# In[']:
                instant_list[0]=code_dict['#@plane']
            instant_table.append(instant_list)
    table_hist_list.append(instant_table)
    
    # remove ignore
    instant_table = []
    for instant_list in table_hist_list[-1]:
        if (instant_list[0] != code_dict['#@ignore']):
            instant_table.append(instant_list)
    table_hist_list.append(instant_table)
    
    # arrange for advance and parameter
    instant_table = []
    for instant_list in table_hist_list[-1]:
        if (instant_list[0]==code_dict['#@advance'])+(instant_list[0]==code_dict['#@r_advance']):
            instant_table.append(instant_list)
    for instant_list in table_hist_list[-1]:
        if (instant_list[0]==code_dict['#@param']):
            instant_table.append(instant_list)
    for instant_list in table_hist_list[-1]:
        if (instant_list[0]==code_dict['#@args']):
            instant_table.append(instant_list)
    for instant_list in table_hist_list[-1]:
        if (instant_list[0]==code_dict['#@default']):
            instant_table.append(instant_list)
    for instant_list in table_hist_list[-1]:
        if (instant_list[0]==code_dict['#@kwargs']):
            instant_table.append(instant_list)
    for instant_list in table_hist_list[-1]:
        if (instant_list[0]==code_dict['#@help']):
            instant_table.append(instant_list)
    for instant_list in table_hist_list[-1]:
        if (instant_list[0]==code_dict['#@plane'])+(instant_list[0]==code_dict['#@return']):
            instant_table.append(instant_list)
    table_hist_list.append(instant_table)
    
    # delete @mark
    instant_table = []
    for instant_list in table_hist_list[-1]:
        if ((instant_list[0]==code_dict['#@param'])*('#@param' == instant_list[1][:len('#@param')])) + ((instant_list[0]==code_dict['#@param'])*(instant_list[1]=='\n')):
            continue
        elif ((instant_list[0]==code_dict['#@args'])*('#@args' == instant_list[1][:len('#@args')])) + ((instant_list[0]==code_dict['#@args'])*(instant_list[1]=='\n')):
            continue
        elif ((instant_list[0]==code_dict['#@default'])*('#@default' == instant_list[1][:len('#@default')])) + ((instant_list[0]==code_dict['#@default'])*(instant_list[1]=='\n')):
            continue
        elif ((instant_list[0]==code_dict['#@kwargs'])*('#@kwargs' == instant_list[1][:len('#@kwargs')])) + ((instant_list[0]==code_dict['#@kwargs'])*(instant_list[1]=='\n')):
            continue
        elif ((instant_list[0]==code_dict['#@advance'])*('#@advance' == instant_list[1][:len('#@advance')])):
            continue
        elif ((instant_list[0]==code_dict['#@r_advance'])*('#@r_advance' == instant_list[1][:len('#@r_advance')])):
            continue
        elif ((instant_list[0]==code_dict['#@help'])*('#@help' == instant_list[1][:len('#@help')])):
            continue
        elif ((instant_list[0]==code_dict['#@plane'])*('#@plane' == instant_list[1][:len('#@plane')])):
            continue
        elif ((instant_list[0]==code_dict['#@return'])*('#@return' == instant_list[1][:len('#@return')])) + ((instant_list[0]==code_dict['#@return'])*(instant_list[1]=='\n')):
            continue
    
        instant_table.append(instant_list)
    table_hist_list.append(instant_table)
    
    # r_advance
    instant_table = []
    for instant_list in table_hist_list[-1]:
        if instant_list[0]==code_dict['#@r_advance']:
            instant_list[1] = instant_list[1].replace('#', '')
            instant_table.append(instant_list)
            continue
        instant_table.append(instant_list)
    table_hist_list.append(instant_table)
    
    # insert tab
    instant_table = []
    old_instant_table = copy.deepcopy(table_hist_list[-1])
    for instant_list in old_instant_table:
        if (instant_list[0]==code_dict['#@plane']):
            instant_list[1] = '    ' + instant_list[1]
        elif (instant_list[0]==code_dict['#@return']):
            return_txt = '\n    '
            check_bool = True
            for chr in instant_list[1]:
                if (chr != ' ')*check_bool:
                    return_txt = return_txt + 'return '
                    check_bool = False
                return_txt = return_txt + chr
            instant_list[1] = return_txt
        elif (instant_list[0]==code_dict['#@help']):
            instant_list[1] = '    ' + instant_list[1]
        
        elif (instant_list[0]==code_dict['#@param'])*('=' in (instant_list[1])):
            instant_list[1] = '    ' + instant_list[1].split('=')[0].replace(' ', '') + ',\n'
        elif (instant_list[0]==code_dict['#@args'])*('=' in (instant_list[1])):
            instant_list[1] = '    *' + instant_list[1].split('=')[0].replace(' ', '') + ',\n'
        elif (instant_list[0]==code_dict['#@default'])*('=' in (instant_list[1])):
            instant_list[1] = '    ' + instant_list[1].replace('\n','').replace(' ', '') + ',\n'
        elif (instant_list[0]==code_dict['#@kwargs'])*('=' in (instant_list[1])):
            instant_list[1] = '    **' + instant_list[1].split('=')[0].replace(' ', '') + ',\n'
        
        elif (instant_list[0]==code_dict['#@param'])*('=' not in (instant_list[1])):
            continue
        elif (instant_list[0]==code_dict['#@args'])*('=' not in (instant_list[1])):
            continue
        elif (instant_list[0]==code_dict['#@kwargs'])*('=' not in (instant_list[1])):
            continue
        instant_table.append(instant_list)
    table_hist_list.append(instant_table)
    
    # setting parameter
    instant_table = []
    old_instant_table = copy.deepcopy(table_hist_list[-1])
    check_num = 0
    for instant_list in old_instant_table:
        if (
            (instant_list[0]==code_dict['#@param']) + 
            (instant_list[0]==code_dict['#@args']) + 
            (instant_list[0]==code_dict['#@default']) + 
            (instant_list[0]==code_dict['#@kwargs']) + 
            (instant_list[0]==code_dict['#@help']) +
            (instant_list[0]==code_dict['#@plane']) +
            (instant_list[0]==code_dict['#@return'])
            )*(check_num==0):
            instant_table.append([0, '\n',-1])
            instant_table.append([0, 'def ' + func_name +'(\n',-1])
            check_num=1    
        if (instant_list[0]!=code_dict['#@param'])*\
            (instant_list[0]!=code_dict['#@args'])*\
            (instant_list[0]!=code_dict['#@default'])*\
            (instant_list[0]!=code_dict['#@kwargs'])*\
            (check_num==1):
    
            instant_table.append([0, '    ):\n',-1])
            instant_table.append(instant_list)
            check_num=2
        else:
            instant_table.append(instant_list)
    table_hist_list.append(instant_table)
    
    with open(func_file_path, 'w') as f:
        for content in table_hist_list[-1]:
            f.write(content[1])

    return func_file_path, func_file_name
