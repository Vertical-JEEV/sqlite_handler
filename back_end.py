
import sqlite3 as sql




class BackEndDB:


    def __init__(self):
        # these are attributes needed to work with a flat file database
        self.db = None
        self.db_name = None
        self.cursor = None
        self.connected_table = None
        self.fields_dict = {}

    # if the databse already has a table we try to get the table name here
    def _connect_db_tables(self):
        try:
            query = '''SELECT name FROM sqlite_master WHERE type="table"'''
            self.cursor.execute(query)

            self.connected_table = self.cursor.fetchall()[0][0]
        except(IndexError):
            self.connected_table = None


    # and if the table does exist then we get the field names and thieir data types
    def _add_db_fields(self):
        query = f"PRAGMA table_info({self.connected_table})"
        self.cursor.execute(query)
        for row in self.cursor.fetchall():
            
            self.fields_dict[row[1]] = row[2]
        


    # we connecte to the databse that the user has selected
    def _connect_db(self,db_path, db_name):
        self.db = sql.connect(db_path)
        self.cursor = self.db.cursor()
        self.db_name = db_name
        self._connect_db_tables()
        if self.connected_table != None:
            self._add_db_fields()


    # here we close and commit the dataase if there is a databse connected
    def _close_db(self):
        if self.db != None:
            self.db.commit()
            self.db.close()
            self.db = None
            self.db_name = None
            self.cursor = None
            self.connected_table = None
            self.fields_dict = {}
        

        

    
    def _create_table(self,table_name, query_fields, fields_dict):
        query = f'''CREATE TABLE {table_name}{query_fields}'''
        self.cursor.execute(query)
        self._connect_db_tables()
        self.fields_dict = fields_dict
        


    def _update_table(self, new_table_name):
        query = f'''ALTER TABLE {self.connected_table} RENAME TO {new_table_name}'''
        self.cursor.execute(query)
        self.connected_table = new_table_name
        self.db.commit()




    def _delete_tables(self):
        query = f"DROP TABLE {self.connected_table}"
        self.cursor.execute(query)
        self._close_db()


        


    def _insert_records(self, values, empty_values_string):
        query = f'''INSERT INTO {self.connected_table} VALUES{empty_values_string}'''
        self.cursor.execute(query, values)
        self.db.commit()



    def _update_record(self, fields_to_update, conditions, values):
        query = f'''UPDATE {self.connected_table} SET {fields_to_update} WHERE {conditions}'''
        self.cursor.execute(query, values)
        self.db.commit()
        


    def _delete_records(self,conditions, values):
        query = f'''DELETE FROM {self.connected_table} WHERE {conditions}'''
        self.cursor.execute(query, values)
        self.db.execute(query, values)
        self.db.commit()

        


    def _view_records(self, query,*values):

        
        if len(values) == 0:
            print(query)
            self.cursor.execute(query)
        else:
            print(values)
            self.cursor.execute(query, values[0])
        fields = [description[0] for description in self.cursor.description]
        records = [record for record in self.cursor]
        self.db.commit()
        return fields, records
        

    

