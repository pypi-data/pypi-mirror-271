import sys
import time
import json
from pyadomd import Pyadomd
import pandas as pd
    
class DependentObjects:
    def __init__(self,recursionlimit = 1000000):
        sys.setrecursionlimit(recursionlimit)
        self.start_time = time.strftime("%H:%M:%S")
        self.calc_dependency_dax_query = r"SELECT [TABLE],[OBJECT],[OBJECT_TYPE],[REFERENCED_TABLE],[REFERENCED_OBJECT],[REFERENCED_OBJECT_TYPE],[REFERENCED_EXPRESSION] FROM $SYSTEM.DISCOVER_CALC_DEPENDENCY where [OBJECT_TYPE] = 'MEASURE' OR [OBJECT_TYPE] = 'CALC_COLUMN' OR [OBJECT_TYPE] = 'CALC_TABLE'"
        self.all_measures_dax_query = r"select [Name] as [parent_object],[Name] as [child_object],[TABLEID] from $SYSTEM.TMSCHEMA_MEASURES"
        self.all_tables_dax_query = r"Select [ID] as [TABLEID],[Name] as [TABLE] from $SYSTEM.TMSCHEMA_TABLES"
        
        
    def time_difference(self,start_time, end_time):
        try:
            # Parse start and end times
            start_h, start_m, start_s = map(int, start_time.split(':'))
            end_h, end_m, end_s = map(int, end_time.split(':'))

            # Convert times to seconds
            start_seconds = start_h * 3600 + start_m * 60 + start_s
            end_seconds = end_h * 3600 + end_m * 60 + end_s

            # Calculate difference
            total_seconds = end_seconds - start_seconds

            # Convert back to hours, minutes, and seconds
            hours, remainder = divmod(total_seconds, 3600)
            minutes, seconds = divmod(remainder, 60)
            
            return f"{hours:02}:{minutes:02}:{seconds:02}"
        except ValueError:
            return "Invalid time format. Please use HH:MM:SS."
  
    def generator_to_list(self,generator_obj):
        result_list = []
        for item in generator_obj:
            result_list.append(item)
            yield item

    def get_nested_child_objects(self,df_ddo,OBJECT):
        child_objects = []
        children = df_ddo[df_ddo['parent_object_tuples'] == OBJECT]
        
        for _, row in children.iterrows():
        #for child in children:
            child_objects.append(row['REFERENCED_OBJECT'])
            child_objects.extend(self.get_nested_child_objects(df_ddo,row['Referenced_Object_Tuples']))
        return child_objects

    def setParams(self,report_name,server,database):
        report_name = report_name
        server = server
        database = database

        connection_string = f'Provider=MSOLAP; Data Source={server};catalog={database};'
    
        # capturing the all dependent objects in the model
        con = Pyadomd(connection_string)
        con.open()
        exe = con.cursor().execute(self.calc_dependency_dax_query)
        generator_obj = exe.fetchone()
        result_generator = self.generator_to_list(generator_obj)
        str = json.dumps(list(result_generator))
        parsed_list = json.loads(str)
        ado = [{"TABLE": item[0], "OBJECT": item[1], "OBJECT_TYPE": item[2], "REFERENCED_TABLE": item[3], "REFERENCED_OBJECT": item[4], "REFERENCED_OBJECT_TYPE": item[5], "REFERENCED_EXPRESSION": item[6] } for item in parsed_list]
        df_ado = pd.DataFrame.from_dict(ado)
        parent_object= df_ado[['TABLE', 'OBJECT', 'OBJECT_TYPE']]
        df_ado['parent_object_tuples'] = parent_object.apply(tuple, axis=1)
        referenced_object = df_ado[['REFERENCED_TABLE', 'REFERENCED_OBJECT', 'REFERENCED_OBJECT_TYPE']]
        df_ado['Referenced_Object_Tuples'] = referenced_object.apply(tuple, axis=1)
        df_ddo = df_ado[df_ado['REFERENCED_OBJECT_TYPE'].isin(['MEASURE','CALC_COLUMN','CALC_TABLE'])]
        df_ddo = df_ddo[['parent_object_tuples', 'Referenced_Object_Tuples', 'OBJECT', 'REFERENCED_OBJECT']]
        con.close()
        
        # capturing the list of measures in the model
        con = Pyadomd(connection_string)
        con.open()
        exe = con.cursor().execute(self.all_measures_dax_query)
        generator_obj = exe.fetchone()
        result_generator = self.generator_to_list(generator_obj)
        str = json.dumps(list(result_generator))
        parsed_list = json.loads(str)
        measurelist = [{"parent_object": item[0], "child_object": item[1],"TABLEID": item[2],"OBJECT_TYPE": "MEASURE"} for item in parsed_list]
        df_measurelist = pd.DataFrame.from_dict(measurelist)
        con.close()  
        
        # capturing the list of tables in the model
        con = Pyadomd(connection_string)
        con.open()
        exe = con.cursor().execute(self.all_tables_dax_query)
        generator_obj = exe.fetchone()
        result_generator = self.generator_to_list(generator_obj)
        str = json.dumps(list(result_generator))
        parsed_list = json.loads(str)
        tablelist = [{"TABLEID": item[0], "TABLE": item[1]} for item in parsed_list]
        df_tablelist = pd.DataFrame.from_dict(tablelist)
        con.close() 
       
        
        df_measurelist = pd.merge(df_measurelist, df_tablelist, how='inner', left_on='TABLEID', right_on='TABLEID')
        measurelist_temp = df_measurelist[['TABLE', 'parent_object', 'OBJECT_TYPE']]
        df_measurelist['parent_object_tuples'] = measurelist_temp.apply(tuple, axis=1)
        df_measurelist['Referenced_Object_Tuples'] = measurelist_temp.apply(tuple, axis=1)
        df_measurelist = df_measurelist[["parent_object_tuples","Referenced_Object_Tuples","parent_object","child_object"]]
       
        # Remove duplicates 
        parent_object = df_ddo.drop_duplicates(subset=['parent_object_tuples','Referenced_Object_Tuples','OBJECT']).copy()    
        
        df_tempbridge = pd.DataFrame(columns=["parent_object_tuples", "Referenced_Object_Tuples","parent_object", "child_object"])
        
        for _, row in parent_object.iterrows():
            all_child_objects = self.get_nested_child_objects(df_ddo,row['parent_object_tuples'])
            temp_df = pd.DataFrame({'parent_object_tuples': [row['parent_object_tuples']]*len(all_child_objects), 'Referenced_Object_Tuples': [row['Referenced_Object_Tuples']]*len(all_child_objects),'parent_object': [row['OBJECT']]*len(all_child_objects) ,'child_object':  all_child_objects})
            df_tempbridge = df_tempbridge._append(temp_df)           
        
        #after recursion appending all measures to bridge
        df_bridge = pd.concat([df_tempbridge, df_measurelist], ignore_index=True)
        df_bridge.to_csv('test.csv')
        
        # Remove duplicates and sort
        df_bridge = df_bridge[["parent_object_tuples","Referenced_Object_Tuples","parent_object","child_object"]]
        df_bridge = df_bridge.drop_duplicates().sort_values(["parent_object_tuples","Referenced_Object_Tuples","parent_object","child_object"]).reset_index(drop=True)        
        
        df_result = pd.merge(df_bridge, df_ado, how='inner', left_on='Referenced_Object_Tuples', right_on='parent_object_tuples')
        df_result = df_result[["parent_object","TABLE","OBJECT","OBJECT_TYPE","REFERENCED_TABLE","REFERENCED_OBJECT","REFERENCED_OBJECT_TYPE","REFERENCED_EXPRESSION"]]
        df_result = df_result.drop_duplicates().sort_values(["parent_object","TABLE","OBJECT","OBJECT_TYPE","REFERENCED_TABLE","REFERENCED_OBJECT","REFERENCED_OBJECT_TYPE","REFERENCED_EXPRESSION"]).reset_index(drop=True)
        
        df_result.to_csv(f"{report_name}_nested_measures.csv")
        
        self.end_time = time.strftime("%H:%M:%S")
        
        print("Execution Time Difference: ", self.time_difference(self.start_time,self.end_time))
              
        return  df_result