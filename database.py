import sqlite3
import os
from typing import Union

def display_current_file_path():
    current_file_path = os.path.abspath(__file__)
    return current_file_path.replace('database.py','')

FOLDER = display_current_file_path().replace('\\','/')

def loading_bar(i:int,lenght:int) -> None:
    """Fonction qui affiche en console une barre de chargement, utile pour les boucles."""
    if lenght != 0:
        state = int(round((i/lenght)*50,0))+1
        on_state = 50-int(state)
        if i == lenght - 1 :
            print('['+"#"*int(state)+" "*int(on_state)+'] : '+str(i+1)+'/'+str(lenght))  
        else:
            print('['+"#"*int(state)+" "*int(on_state)+'] : '+str(i+1)+'/'+str(lenght),end="\r") 

def add_column_to_table(db:str, table_name:str, column_name:str, column_type:str) -> None:
    """Add a new column to the given table."""
    conn = sqlite3.connect(db)
    cursor = conn.cursor()
    try:
        cursor.execute(f"ALTER TABLE {table_name} ADD COLUMN {column_name} {column_type}")
    except Exception as e:
        print(e)   
    conn.commit()
    conn.close()

def create_table(db:str, table_name:str, columns:dict) -> None:
    """Create a new table in the given database."""
    conn = sqlite3.connect(db)
    cursor = conn.cursor()

    column_definitions = ", ".join([f"{key} {value}" for key, value in columns.items()])
    cursor.execute(f"CREATE TABLE IF NOT EXISTS {table_name} (id INTEGER PRIMARY KEY, {column_definitions})")
    conn.commit()
    conn.close()

def insert_data(db:str, table_name:str, data:dict) -> int:
    """Insert data into the given table."""
    conn = sqlite3.connect(db)
    cursor = conn.cursor()

    columns = ", ".join(data.keys())
    values = ", ".join(["?" for _ in data.values()])

    cursor.execute(f"INSERT INTO {table_name} ({columns}) VALUES ({values})", tuple(data.values()))
    
    conn.commit()
    conn.close()
    
    return cursor.lastrowid

def get_data(db:str, table_name:str, condition:str = "") -> list:
    """Retrieve data from the given table based on the provided condition."""
    conn = sqlite3.connect(db)
    cursor = conn.cursor()

    if condition is "":
        cursor.execute(f"SELECT * FROM {table_name}")
    else:
        cursor.execute(f"SELECT * FROM {table_name} WHERE {condition}")
    data = cursor.fetchall()

    conn.close()

    return [list(row) for row in data]

def delete_data(db:str, table_name:str, condition:str) -> None:
    """Delete data from the given table based on the provided condition."""
    conn = sqlite3.connect(db)
    cursor = conn.cursor()

    cursor.execute(f"DELETE FROM {table_name} WHERE {condition}")
    conn.commit()

    conn.close()

def update_data(db:str, table_name:str, data:dict, condition:str) -> None:
    """Update data in the given table based on the provided condition."""
    conn = sqlite3.connect(db)
    cursor = conn.cursor()

    set_values = ", ".join([f"{key} = ?" for key in data.keys()])

    cursor.execute(f"UPDATE {table_name} SET {set_values} WHERE {condition}", tuple(data.values()))
    
    conn.commit()

    conn.close()

def mega_insert(db:str, table_name:str, data:list) -> None:
    """Insert a large amount of data into the given table."""

    print(f"Mega Insert en cours... {table_name} | {len(data)} lignes.")

    if len(data) > 1000:
        print("Split des data") 
        list_result = []  

        for i in range(0,len(data),1000):
            if i+1000 > len(data):
                list_result.append(data[i:])
            else:
                list_result.append(data[i:i+1000])     

        for d in list_result:
            conn = sqlite3.connect(db)
            cursor = conn.cursor()
            for row in d:
                columns = ", ".join(row.keys())
                values = ", ".join(["?" for _ in row.values()])
                cursor.execute(f"INSERT INTO {table_name} ({columns}) VALUES ({values})", tuple(row.values()))
                
            print(f"Mega Insert {list_result.index(d)}/{len(list_result)} terminé... | {len(d)} {table_name}.")
        
            conn.commit()
            conn.close()
    else:
        conn = sqlite3.connect(db)
        cursor = conn.cursor()
        for row in data:
            columns = ", ".join(row.keys())
            values = ", ".join(["?" for _ in row.values()])
            cursor.execute(f"INSERT INTO {table_name} ({columns}) VALUES ({values})", tuple(row.values()))
            
        print(f"Mega Insert terminé... | {len(data)} {table_name}.")
    
        conn.commit()
        conn.close()     

def create_class(db:str) -> None:
    test = get_data(db, "sqlite_master")
    text_remove = ["CREATE TABLE","INTEGER PRIMARY KEY","INTEGER","TEXT","NONE","REAL","NUMERIC"]
    models = f"from database import *\n\nDATABASE = '{f'{db}'}'\n"
    
    tables = {}
    for row in test:
        data = row[-1]
        for text in text_remove:
            data = data.replace(text,"")
        table_name = str(row[1])
        columns = data.split('(')[1].replace(')','').split(',')
        tables[table_name] = {}
        tables[table_name]['columns'] = [column.strip() for column in columns]
        tables[table_name]['child'] = []
        tables[table_name]['parent'] = []
    for ct in tables:
        for c in tables[ct]['columns']:
            if "_id" in c:
                obj = [c,c.replace('_id','')]
                tables[ct]['parent'].append(obj)
        #print(ct)
        for t in tables:
            for c in tables[t]['columns']:
                if ct+"_id" == c:
                    obj = [t,c]
                    tables[ct]['child'].append(obj)
                    
    for row in test:
        data = row[-1]
        for text in text_remove:
            data = data.replace(text,"")
        table_name = row[1]
        columns = data.split('(')[1].replace(')','').split(',')
        columns_type = row[-1].split('(')[1].replace(')','').split(',')
        columns = [column.strip() for column in columns]
        columns_without_id = columns.copy()
        columns_without_id.remove("id") if "id" in columns else None
        columns_input = []
        for c in columns_without_id:
            for ct in columns_type:
                if c in ct:
                    if "INTEGER" in ct:
                        columns_input.append(f"{c}:int")
                    elif "TEXT" in ct:
                        columns_input.append(f"{c}:str")
                    elif "REAL" in ct:
                        columns_input.append(f"{c}:float")
                    elif "NUMERIC" in ct:
                        columns_input.append(f"{c}:float")
        columns_self = [f"self.{column} = {column}\n        " for column in columns]
        columns_with_type = ["        "+column.replace(':'," (")+")\n" for column in columns_input]
        class_ = f"""
class {table_name.capitalize()}:
    \"\"\"
    Class for accessing data from table "{table_name}".
    \"\"\"
    def __init__(self, {', '.join(columns_input)}{", id:int = 0" if "id" in columns else None}) -> None:
        \"\"\"
        Initialize a new instance of the Model class.

        Args:
{''.join(columns_with_type)}        id (int, optional): Defaults to 0.
        \"\"\"
        {''.join(columns_self)}\n"""
        parent_list = [f"{p[1]}" for p in tables[table_name]['parent']]
        child_list = [f"{p[0]}" for p in tables[table_name]['child']]
        for p in tables[table_name]['parent']:
            class_ += f"""        self.{p[1]} = None\n"""
        for p in tables[table_name]['child']:
            class_ += f"""        self.{p[0]} = []\n"""
        class_ += f"""
    def insert(self, db:str = DATABASE) -> None:
        \"\"\"
        Inserts the {table_name.capitalize()} object into the specified database.
        Only works if the self.id is not 0.

        Args:
            db (str): The name of the database to insert the participant into.

        Returns:
            None
        \"\"\"
        if self.id == 0:
            withou_id = self.__dict__.copy()
            del withou_id['id']{''.join([f";del withou_id['{i}']" for i in parent_list])}{''.join([f";del withou_id['{i}']" for i in child_list])}
            self.id = insert_data(db, "{table_name}", withou_id)
    """
        class_ += f"""
    def update(self, db:str = DATABASE) -> None:
        \"\"\"
        Updates the {table_name.capitalize()} object in the database.

        Args:
            db (str): The name of the database to update the object in.

        Returns:
            None
        \"\"\"
        if self.id != 0:
            withou_id = self.__dict__.copy()
            del withou_id['id']{''.join([f";del withou_id['{i}']" for i in parent_list])}{''.join([f";del withou_id['{i}']" for i in child_list])}
            update_data(db, "{table_name}", withou_id, f"id = {'{self.id}'}")
    """
        class_ += f"""
    def delete(self, db:str = DATABASE) -> None:
        \"\"\"
        Deletes the {table_name.capitalize()} object from the specified database.

        Args:
            db (str): The name of the database to delete the object from.

        Returns:
            None
        \"\"\"
        delete_data(db, "{table_name}", f"id = {'{self.id}'}")
    """
        if len(tables[table_name]['child']) != 0:
            for child in tables[table_name]['child']:
                class_ += f"""
    def get_{child[0]}(self, db:str = DATABASE) -> None:
        \"\"\"
        Retrieves the {child[0].capitalize()} associated with the current {table_name.capitalize()} from the database.

        Args:
            db (str): The name of the database to query. Defaults to the value of the DATABASE constant.

        Returns:
            None
        \"\"\"
        self.{child[0]} = get_{child[0]}(db, f"{child[1]} = {'{self.id}'}")
                """
                
        if len(tables[table_name]['parent']) != 0:
            for child in tables[table_name]['parent']:
                class_ += f"""
    def get_{child[1]}(self, db:str = DATABASE) -> None:
        \"\"\"
        Retrieves the {child[1].capitalize()} from the database based on the {child[1]}_id in the current {table_name.capitalize()} object.

        Args:
            db (str): The name of the database to query. Defaults to DATABASE.

        Returns:
            None
        \"\"\"
        self.{child[1]} =  get_{child[1]}(db, f"id = {'{'}self.{child[0]}{'}'}", first=True)
                """
        models += class_

    for row in test:
        data = row[-1]
        for text in text_remove:
            data = data.replace(text,"")
        table_name = row[1]
        columns = data.split('(')[1].replace(')','').split(',')
        columns_type = row[-1].split('(')[1].replace(')','').split(',')
        columns = [column.strip() for column in columns]
        columns_input = []
        columns_without_id = columns.copy()
        columns_without_id.remove("id") if "id" in columns else None
        for c in columns:
            for ct in columns_type:
                if c in ct:
                    if "INTEGER" in ct:
                        columns_input.append(f"{c}:int")
                    elif "TEXT" in ct:
                        columns_input.append(f"{c}:str")
                    elif "REAL" in ct:
                        columns_input.append(f"{c}:float")
                    elif "NUMERIC" in ct:
                        columns_input.append(f"{c}:float")
        columns_self = [f"self.{column} = {column}\n\t" for column in columns]
        class_ = f"""
def get_{table_name}(db:str = DATABASE, condition:str = "", first:bool = False, count:bool = False) -> Union[list, {table_name.capitalize()}, int, None]:
    \"\"\"
    Args:
        db (string, optional): Database path. Defaults to DATABASE.
        condition (string, optional): Condition for query. Defaults to None.
        first (bool, optional): If true return only the first result. Defaults to False.
        count (bool, optional): If true return integer of result. Defaults to False.
    
    Return:
        Union[list, {table_name.capitalize()}, int, None]: 
            - If first is True, returns a single {table_name.capitalize()} object or None if no result is found.
            - If count is True, returns the integer count of results.
            - Otherwise, returns a list of {table_name.capitalize()} objects.
    \"\"\"
    data_list = get_data(db, "{table_name}", condition)
    if first:
        return {table_name.capitalize()}({','.join([f"{columns[i]} = data_list[0][{i}]" for i in range(len(columns_self))])}) if len(data_list) != 0 else None
    if count:
        return len(data_list)
    return [{table_name.capitalize()}({','.join([f"{columns[i]} = l[{i}]" for i in range(len(columns_self))])}) for l in data_list]
        """
        models += class_

    with open(f"{FOLDER}/models.py","w") as file:
        file.write(models)        