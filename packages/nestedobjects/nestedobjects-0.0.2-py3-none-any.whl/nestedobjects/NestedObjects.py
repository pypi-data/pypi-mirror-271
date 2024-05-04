import glob
import pandas as pd
import sys
import time
import json
import warnings

pd.options.mode.chained_assignment = None  # default='warn'

def set_parameters(data_source,folder_path = None, adomd_path = "\\Program Files\\Microsoft.NET\\ADOMD.NET\\160", server = None, database = None, filename = None):
    if folder_path is not None or (server is not None and database is not None):
        dataframes = get_data(data_source= data_source,folder_path= folder_path,server = server,database = database,adomd_path = adomd_path)
        result = nestedobjects(dataframes)
        result.to_csv(f"{filename}_nested_objects.csv")
        print(result)
    else: 
        print("You have two options for selecting a data source.")
        print("If you choose csv as your data source, please provide the path to the csv file you wish to import.")
        print("Alternatively, if you select Database as your data source, please provide the ADOMD path located in your system to establish a connection to Analysis Services. Please provide the server and database details of the powerbi dataset or analysis services or local host")
            
def get_nested_child_objects(direct_dependent_objects,OBJECT):
        child_objects = []
        children = direct_dependent_objects[direct_dependent_objects['parent_object_tuples'] == OBJECT]
        
        for _, row in children.iterrows():
            child_objects.append(row['REFERENCED_OBJECT'])
            child_objects.extend(get_nested_child_objects(direct_dependent_objects,row['referenced_object_tuples']))
        return child_objects

def get_data(data_source,folder_path = None, adomd_path = "\\Program Files\\Microsoft.NET\\ADOMD.NET\\160", server = None, database = None): 
    
    if data_source == "folder" and folder_path is not None:
        
        csv_files = glob.glob(f"{folder_path}/*.csv")
        
        for file in csv_files:
            try:
                if "tables.csv" in file:
                    tables = pd.read_csv(file)
                elif "measures.csv" in file:
                    measures = pd.read_csv(file)
                elif "calc_dependency.csv" in file:
                    calc_dependency = pd.read_csv(file)
                else:
                    print("Required files are not found")
            except PermissionError:
                print(f"Error: Permission denied for file {file}")
        
        return {"tables": tables, "measures": measures, "calc_dependency": calc_dependency}
        
    elif data_source == "live" and server is not None and database is not None:
        
        calc_dependency_dax_query = r"SELECT * FROM $SYSTEM.DISCOVER_CALC_DEPENDENCY"
        measures_dax_query = r"select * from $SYSTEM.TMSCHEMA_MEASURES"
        tables_dax_query = r"Select * from $SYSTEM.TMSCHEMA_TABLES"
        
        from sys import path
        path.append(adomd_path)
        from pyadomd import Pyadomd
        
        connection_string = f'Provider=MSOLAP; Data Source={server};catalog={database};'
        
        con = Pyadomd(connection_string)
        con.open()
        exe = con.cursor().execute(calc_dependency_dax_query)
        calc_dependency = pd.DataFrame(exe.fetchone())
        calc_dependency.columns = ["DATABASE_NAME", "OBJECT_TYPE", "TABLE", "OBJECT", "EXPRESSION", "REFERENCED_OBJECT_TYPE", "REFERENCED_TABLE", "REFERENCED_OBJECT", "REFERENCED_EXPRESSION", "QUERY"]
        con.close()
        
        con = Pyadomd(connection_string)
        con.open()
        exe = con.cursor().execute(measures_dax_query)
        measures = pd.DataFrame(exe.fetchone())
        measures.columns = ["ID","TableID", "Name", "Description",	"DataType", "Expression", "FormatString", "IsHidden","State","ModifiedTime","StructureModifiedTime","KPIID","IsSimpleMeasure","ErrorMessage","DisplayFolder","DetailRowsDefinitionID","DataCategory","LineageTag","SourceLineageTag"]
        con.close()
        
        con = Pyadomd(connection_string)
        con.open()
        exe = con.cursor().execute(tables_dax_query)
        tables = pd.DataFrame(exe.fetchone())
        tables.columns = ["ID","ModelID","Name","DataCategory","Description","IsHidden","TableStorageID","ModifiedTime","StructureModifiedTime","SystemFlags","ShowAsVariationsOnly","IsPrivate","DefaultDetailRowsDefinitionID","AlternateSourcePrecedence","RefreshPolicyID","CalculationGroupID","ExcludeFromModelRefresh","LineageTag","SourceLineageTag","SystemManaged"]
        con.close()
        return {"tables": tables, "measures": measures, "calc_dependency": calc_dependency}
        
    else: 
        print("You have two options for selecting a data source.")
        print("If you choose csv as your data source, please provide the path to the csv file you wish to import.")
        print("Alternatively, if you select Database as your data source, please provide the ADOMD path located in your system to establish a connection to Analysis Services. Please provide the server and database details of the powerbi dataset or analysis services or local host")
        return None

def nestedobjects(dataframes): 
    tables = dataframes["tables"]
    measures = dataframes["measures"]
    calc_dependency = dataframes["calc_dependency"]
    
    tables = tables[['ID','Name']]
    calc_dependency = calc_dependency[calc_dependency['OBJECT_TYPE'].isin(['MEASURE','CALC_COLUMN','CALC_TABLE'])]
     
    calc_dependency['parent_object_tuples'] = calc_dependency[['TABLE', 'OBJECT', 'OBJECT_TYPE']].apply(tuple, axis=1)
    calc_dependency['referenced_object_tuples'] = calc_dependency[['REFERENCED_TABLE', 'REFERENCED_OBJECT', 'REFERENCED_OBJECT_TYPE']].apply(tuple, axis=1)
    
    measures = pd.merge(measures, tables, how='inner', left_on='TableID', right_on='ID')
    measures.rename(columns={'Name_y': 'TABLE'}, inplace=True)
    measures.rename(columns={'Name_x': 'Name'}, inplace=True)
    measures.rename(columns={'ID_x': 'ID'}, inplace=True)
    
    
    direct_dependent_objects = calc_dependency[calc_dependency['REFERENCED_OBJECT_TYPE'].isin(['MEASURE','CALC_COLUMN','CALC_TABLE'])]
    direct_dependent_objects = direct_dependent_objects[['parent_object_tuples', 'referenced_object_tuples', 'OBJECT', 'REFERENCED_OBJECT']]
    
    measures_modified = pd.DataFrame(columns=["TABLE","parent_object","child_object","OBJECT_TYPE"])
    measures_modified["TABLE"] = measures["TABLE"]
    measures_modified["parent_object"] = measures["Name"]
    measures_modified["child_object"] = measures["Name"]
    measures_modified["OBJECT_TYPE"] = "MEASURE"
    measures_modified['parent_object_tuples'] = measures_modified[['TABLE', 'parent_object', 'OBJECT_TYPE']].apply(tuple, axis=1)
    measures_modified['referenced_object_tuples'] = measures_modified[['TABLE', 'parent_object', 'OBJECT_TYPE']].apply(tuple, axis=1)
    measures_modified = measures_modified[["parent_object_tuples","referenced_object_tuples","parent_object","child_object"]]
    
    nested_objects = pd.DataFrame(columns=["parent_object_tuples", "referenced_object_tuples","parent_object", "child_object"])
    
    for _, row in direct_dependent_objects.iterrows():
            all_child_objects = get_nested_child_objects(direct_dependent_objects,row['parent_object_tuples'])
            dataframe_temp = pd.DataFrame({'parent_object_tuples': [row['parent_object_tuples']]*len(all_child_objects), 'referenced_object_tuples': [row['referenced_object_tuples']]*len(all_child_objects),'parent_object': [row['OBJECT']]*len(all_child_objects) ,'child_object':  all_child_objects})
            nested_objects = nested_objects._append(dataframe_temp)
            
    #after recursion appending all measures to bridge
    nested_objects = pd.concat([nested_objects, measures_modified], ignore_index=True)
    
    # Remove duplicates and sort
    nested_objects = nested_objects.drop_duplicates().sort_values(["parent_object_tuples","referenced_object_tuples","parent_object","child_object"]).reset_index(drop=True) 
    
    nested_objects = pd.merge(nested_objects, calc_dependency, how='inner', left_on='referenced_object_tuples', right_on='parent_object_tuples')
    nested_objects = nested_objects[["parent_object","TABLE","OBJECT","OBJECT_TYPE","REFERENCED_TABLE","REFERENCED_OBJECT","REFERENCED_OBJECT_TYPE","REFERENCED_EXPRESSION"]]
    nested_objects = nested_objects.drop_duplicates().sort_values(["parent_object","TABLE","OBJECT","OBJECT_TYPE","REFERENCED_TABLE","REFERENCED_OBJECT","REFERENCED_OBJECT_TYPE","REFERENCED_EXPRESSION"]).reset_index(drop=True)
    nested_objects["Parent_child"] = "Child"
    nested_objects = nested_objects.reindex(columns= ["Parent_child","parent_object","TABLE","OBJECT","OBJECT_TYPE","REFERENCED_TABLE","REFERENCED_OBJECT","REFERENCED_OBJECT_TYPE","REFERENCED_EXPRESSION"])
    
    #readding the parent measures in the nested objects
    measures_modified1 = pd.DataFrame(columns=["Parent_child","parent_object","TABLE","OBJECT","OBJECT_TYPE","REFERENCED_TABLE","REFERENCED_OBJECT","REFERENCED_OBJECT_TYPE","REFERENCED_EXPRESSION"])
    measures_modified1["parent_object"] = measures["Name"]
    measures_modified1["TABLE"] = measures["TABLE"]
    measures_modified1["OBJECT"] = measures["Name"]
    measures_modified1["OBJECT_TYPE"] = "MEASURE"
    measures_modified1["REFERENCED_TABLE"] = measures["TABLE"]
    measures_modified1["REFERENCED_OBJECT"] = measures["Name"]
    measures_modified1["REFERENCED_OBJECT_TYPE"] = "MEASURE"
    measures_modified1["REFERENCED_EXPRESSION"] = measures["Expression"]
    measures_modified1["Parent_child"] = "Parent"
    #readding the calc column and table objects
    calc_dependency = calc_dependency[calc_dependency['OBJECT_TYPE'].isin(['CALC_COLUMN','CALC_TABLE'])]
    calc_dependency = calc_dependency[["TABLE","OBJECT","OBJECT_TYPE","EXPRESSION"]].drop_duplicates()
    calc_dependency_modified = pd.DataFrame(columns=["Parent_child","parent_object","TABLE","OBJECT","OBJECT_TYPE","REFERENCED_TABLE","REFERENCED_OBJECT","REFERENCED_OBJECT_TYPE","REFERENCED_EXPRESSION"])
    calc_dependency_modified["parent_object"] = calc_dependency["OBJECT"]
    calc_dependency_modified["TABLE"] = calc_dependency["TABLE"]
    calc_dependency_modified["OBJECT"] = calc_dependency["OBJECT"]
    calc_dependency_modified["OBJECT_TYPE"] = calc_dependency["OBJECT_TYPE"]
    calc_dependency_modified["REFERENCED_TABLE"] = calc_dependency["TABLE"]
    calc_dependency_modified["REFERENCED_OBJECT"] = calc_dependency["OBJECT"]
    calc_dependency_modified["REFERENCED_OBJECT_TYPE"] = calc_dependency["OBJECT_TYPE"]
    calc_dependency_modified["REFERENCED_EXPRESSION"] = calc_dependency["EXPRESSION"]
    calc_dependency_modified["Parent_child"] = "Parent"
    
    nested_objects1 = pd.concat([nested_objects, measures_modified1,calc_dependency_modified], ignore_index=True)
    nested_objects1 = nested_objects1.sort_values(["parent_object","Parent_child","TABLE","OBJECT","OBJECT_TYPE","REFERENCED_TABLE","REFERENCED_OBJECT","REFERENCED_OBJECT_TYPE","REFERENCED_EXPRESSION"], ascending=[True, False, True, True, True, True, True, True, True]).reset_index(drop=True)

    return nested_objects1