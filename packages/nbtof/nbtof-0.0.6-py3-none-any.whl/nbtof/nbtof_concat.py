import ast, copy
import numpy as np
import pandas as pd
import os
import warnings


def body_dig(node, i = -1):
    return_name_table = []
    for j, node_u in enumerate(node.body):
        if type(node_u) == ast.Import:
            for name in node_u.names:
                if name.asname is not None:
                    return_name_table.append([name.asname, j * (i<0) + i * (i>=0), type(node_u), None, name.name, name.asname, None])
                else:
                    return_name_table.append([name.name, j * (i<0) + i * (i>=0), type(node_u), None, name.name, name.asname, None])
        elif type(node_u) == ast.ImportFrom:
            level = node_u.level
            for name in node_u.names:
                if name.asname is not None:
                    return_name_table.append([name.asname, j * (i<0) + i * (i>=0), type(node_u), node_u.module, name.name, name.asname, level])
                else:
                    return_name_table.append([name.name, j * (i<0) + i * (i>=0), type(node_u), node_u.module, name.name, name.asname, level])
        elif type(node_u) == ast.Assign:
            if type(node_u.targets[0]) == ast.Tuple:
                for elt in node_u.targets[0].elts:
                    #return_name_table.append(elt.id)
                    return_name_table.append([elt.id, j * (i<0) + i * (i>=0), type(node_u), None, None, None, None])
            elif type(node_u.targets[0]) == ast.Name:
                return_name_table.append([node_u.targets[0].id, j * (i<0) + i * (i>=0), type(node_u), None, None, None, None])
        elif type(node_u) == ast.For:
            if type(node_u.target) == ast.Tuple:
                for elt in node_u.target.elts:
                    #return_name_table.append(elt.id)
                    return_name_table.append([elt.id, j * (i<0) + i * (i>=0), type(node_u), None, None, None, None])
            elif type(node_u.target) == ast.Name:
                #return_name_table.append(node_u.target.id)
                return_name_table.append([node_u.target.id, j * (i<0) + i * (i>=0), type(node_u), None, None, None, None])

            return_name_table = return_name_table + body_dig(node_u, j * (i<0) + i * (i>=0))
        
        elif type(node_u) == ast.FunctionDef:
            return_name_table.append([node_u.name, j * (i<0) + i * (i>=0), type(node_u), None, None, None, None])
        elif type(node_u) == ast.While:
            return_name_table = return_name_table + body_dig(node_u, j * (i<0) + i * (i>=0))
        elif type(node_u) == ast.Try:
            return_name_table = return_name_table + body_dig(node_u, j * (i<0) + i * (i>=0))
            for handler in node_u.handlers:
                return_name_table = return_name_table + body_dig(handler, j * (i<0) + i * (i>=0))               
        elif type(node_u) == ast.If:
            return_name_table = return_name_table + body_dig(node_u, j * (i<0) + i * (i>=0))
    return return_name_table
def name_info_df(func_p):
    func_name_table = body_dig(func_p)
    if func_name_table == []:
        return_name_df = pd.DataFrame(
            columns=['name', 'idx', 'type', 'module', 'import', 'as', "level"]
        )
    else:
        return_name_df = pd.DataFrame(
            data=np.array(func_name_table),
            columns=['name', 'idx', 'type', 'module', 'import', 'as', "level"]
        )
    return return_name_df
def import_str(name_ds):
    if name_ds['module'] is not None:
        return name_ds['module'] + '.' + name_ds['import']
    else:
        return name_ds['import']
def new_import_check(add_name_ds, base_name_df):
    #add_import_info_alist = add_name_df.iloc[4][['module', 'import', 'as']].values
    #base_import_info_array = base_name_df[['module', 'import', 'as']].values
    concat_status = 'new'
    for _, base_name_ds in base_name_df.iterrows():
        if (add_name_ds['name'] == base_name_ds['name'])*(import_str(add_name_ds) == import_str(base_name_ds))*(add_name_ds["level"] == base_name_ds["level"]):
            concat_status = 'same_import'
        elif (add_name_ds['name'] == base_name_ds['name'])*((import_str(add_name_ds) != import_str(base_name_ds))+(add_name_ds["level"] == base_name_ds["level"])):
            concat_status = 'error'
    return concat_status

def nbtof_concat(
    base_py_path:str,
    add_py_path:str,
    concatenated_py_path:str=None,
    auto_sort:bool=True,
    func_update:bool=False,
    ):
    
    if base_py_path[-3:] != '.py':
        base_py_path = base_py_path +'.py'
    if add_py_path[-3:] != '.py':
        add_py_path = add_py_path +'.py'
    
    if concatenated_py_path is None:
        concatenated_py_path = base_py_path
    elif concatenated_py_path is not None:
        if concatenated_py_path[-3:] != '.py':
            concatenated_py_path = concatenated_py_path +'.py'
    
    #if not os.path.isfile(base_py_path):
    #    with open(base_py_path, 'w') as f:
    #        pass
    
    with open(base_py_path) as f:
        base_p = copy.deepcopy(ast.parse(f.read()))
    with open(add_py_path) as f:
        add_p = copy.deepcopy(ast.parse(f.read()))
    
    base_name_df = name_info_df(base_p)
    add_name_df = name_info_df(add_p)
    
    return_p = copy.deepcopy(base_p)
    return_body_list = []
    for idx, node in enumerate(add_p.body):
        instant_name_df = add_name_df[add_name_df['idx'] == idx]
        if (type(node) == ast.Import):
            for _, instant_name_ds in instant_name_df.iterrows():
                concat_status = new_import_check(instant_name_ds, base_name_df)
                if (concat_status == 'new'):
                    instant_module = ast.Import(
                        names=[
                            ast.alias(
                                name = instant_name_ds['import'], 
                                asname=instant_name_ds['as']
                                )
                            ]
                        )
                    return_body_list.append(copy.deepcopy(instant_module))
        elif (type(node) == ast.ImportFrom):
            for _, instant_name_ds in instant_name_df.iterrows():
                concat_status = new_import_check(instant_name_ds, base_name_df)
                if (concat_status == 'new'):
                    instant_module = ast.ImportFrom(
                        module=instant_name_ds['module'],
                        names=[
                            ast.alias(
                                name = instant_name_ds['import'], 
                                asname=instant_name_ds['as'],
                                )
                            ],
                        level=instant_name_ds['level']
                        )
                    return_body_list.append(copy.deepcopy(instant_module))
        elif (type(node) == ast.FunctionDef):
            add_func_name = add_name_df[(add_name_df['idx'] == idx)&(add_name_df['type'] == ast.FunctionDef)]['name'].values[0]
            return_body_list.append(copy.deepcopy(node))
            for _, instant_name_ds in base_name_df.iterrows():
                if (instant_name_ds['name'] == add_func_name)*(instant_name_ds['type'] == ast.FunctionDef):
                    if func_update == False:
                        warnings.warn(f"There is the same function name \"{add_func_name}\" in several files. If you want to replace function, plase set \"func_update\" True.")
                        return_body_list = return_body_list[:-1]
                    elif func_update == True:
                        return_p.body[instant_name_ds['idx']] = copy.deepcopy(node)
                        return_body_list = return_body_list[:-1]        
                    break
                elif (instant_name_ds['name'] == add_func_name)*(instant_name_ds['type'] == ast.Assign):
                    warnings.warn(f"function name \"{add_func_name}\" in \"{add_py_path}\" is already used as variable name in other file.")
                elif (instant_name_ds['name'] == add_func_name)*((instant_name_ds['type'] == ast.Import) + (instant_name_ds['type'] == ast.ImportFrom)):
                    warnings.warn(f"function name \"{add_func_name}\" in \"{add_py_path}\" is already used as imported module name in other file.")
        else:
            return_body_list.append(copy.deepcopy(node))
            
    return_p.body = return_p.body + return_body_list
    
    if auto_sort:
        auto_sort_table = [
            [ast.Import], 
            [ast.ImportFrom],
            [ast.Assign, ast.AnnAssign, ast.For, ast.AsyncFor, ast.While, ast.Raise, ast.If, ast.ClassDef, ast.With, ast.Expr],
            [ast.FunctionDef, ast.AsyncFunctionDef],
            [ast.Delete, ast.Return, ast.Break, ast.Continue, ast.Pass],
            ]
        sort_body_list = []
        for auto_sort_list in auto_sort_table:
            for node in return_p.body:
                if type(node) in auto_sort_list:
                    sort_body_list.append(copy.deepcopy(node))
        return_p.body = sort_body_list
    
    with open(base_py_path, mode='w') as f:
        f.write(ast.unparse(return_p))

    return True
