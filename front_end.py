import os
from tkinter import filedialog as fd
from back_end import BackEndDB
from time import sleep




SLEEP_TIME = 1

class InputHandler:


    # different sqlite data types for fields
    DATA_TYPES = ["TEXT", "NULL", "REAL", "BLOB", "INTEGER"]


    def string_check(self, string):
        # check if it is alphanumeric≠≠
       return True if string.isalnum() else False


    def num_check(self, value, condition):
        # check if it valid float or integer
        # the integer is for checking if the correct option was inputted
        try:
            if condition:
                float(value)
            else:
                int(value)
            return True
        except ValueError:
            return False


    # check if its a valid field data type
    def valid_data_type(self, data_type):
        return True if data_type in self.DATA_TYPES else False




    def valid_value(self, data_type, value):
        valid = True
        # these are for checking if the values match the corressponding data value
        if data_type == "TEXT":
            valid = True if value.isascii() else False
        elif data_type == "REAL":
            valid  = self.num_check(value, True)
        elif data_type == "INTEGER":
            valid = True if value.isnumeric() else False
        return valid 



    def valid_file(self,file_path, needed_ext):
        # check if it is a valid file
        ext = os.path.splitext(str(file_path))[1]
        return True if ext.split("'",1)[0] ==  needed_ext else False










class FrontEndDB:
    def __init__(self):
        # this connects to our input handler and our backandDB
        self.VALID = InputHandler()
        self.BACK_DB = BackEndDB()
        




    def _are_you_happy(self, string, condition):

        # this function gets the user input whether they are happy of not, if they are not happy the user gets to re-input their, fields, values etc
        while True:
            print(f"Your condition is: {condition}\n")
            print(f"Press 1 if you are happy {string}\n")
            print(f"Press 2 if you are not happy {string}\n")
            yes_or_no = input("Which number do you choose\n")
            if self.VALID.num_check(yes_or_no, False):
                return True if int(yes_or_no) == 1 else False
            else:
                print("Invalid input, try again\n")





    def _which_fields(self, string):
        # it gets the users fields and data types from the users table and adds them to a dict
        needed_fields= {}
        # this for getting the question marks and their field names
        needed_fields_str = '('
        empty_fields ='('


        for field, field_type in self.BACK_DB.fields_dict.items():

            print(f"The current field is: {field}\n")
            sleep(0.25)
            print(f"Press 1 if you want to {string}\n")
            sleep(0.25)
            print(f"Press 2 if you dont want {string}\n")
    
           # in this while loop, we get the users fields either for updating, viewing specifc fields or being used as conditions
            while True:
                add_or_not = input("Enter your number\n")
                if self.VALID.num_check(add_or_not, False):
                    if add_or_not == "1":

                        # these generates, fields and their data types, string: "(field1, field2, field3, field3,........") and "(?,?,?,?,?)"
                        needed_fields[field] = field_type
                        needed_fields_str += (field +',')
                        empty_fields += ("?,")
                    break
                else:
                    print("Invalid option, try again\n")


        

        # removes the last comma 
        needed_fields_str = ((needed_fields_str[:len(needed_fields_str)-1] + "" + needed_fields_str[len(needed_fields_str):]) + ")") 
        empty_fields_str = empty_fields[:len(empty_fields)-1] + "" + empty_fields[len(empty_fields):]+')'


        # check if the user is happy with their fields if not, recalls this fucntion
        if not self._are_you_happy("with these fields", needed_fields):
            needed_fields, needed_fields_str, empty_fields_str = self._which_fields(string)
            
        
        return needed_fields, needed_fields_str, empty_fields_str









    def _get_conditions(self, fields):
    
        condition_str = ''
        # it gets the condtion it AND, OR after each field , makes a condition

        # this loop through the fields, we track of the count using enumerate because if there are n3 fields we can only add 2 condition operators ie, the number of operator you can add is always 1 less than the number of fields
        for count,field in enumerate(fields):
            print(count)

            if count ==(len(fields)-1):
                end_field = list(fields)[-1]
                condition_str += f'{end_field} = ?'
                break


            while True:
                #this generates the condition string with the users chosen booloean operator
                print(f"Press 1 to add 'AND' after your field {field}\n")
                print(f"Press 2 to add 'OR' after your field {field}\n")
                boolean_op = input("Which boolean operator do you want to use\n")
                if self.VALID.num_check(boolean_op, False):
                    if 1<=int(boolean_op)<=2:
                        boolean_op = "AND" if int(boolean_op) == 1 else "OR"
                        condition_str += f'{field} = ? {boolean_op} '
                        break
                    else:
                        print("Invalid option, try again\n")
                else:
                    print("Invalid option, try again\n")


        if not self._are_you_happy("with the condition", condition_str):
            condition_str = self._get_conditions(fields)

        return condition_str


            
    def _get_values(self, fields, string):
        # this loops through your fields  and gets the values for them, it also checks if it matches the fields types data 
        values = []
        
        # the looping through the dictionary gets us our field and their corresponding data type
        for field_name, data_type in fields.items():
            while True:
                # get the input for each field, validating it as well
                value = input(string+f" {field_name}\n")
                # this means that we can pass in our value and data type  and checks if they match
                if self.VALID.valid_value(data_type, value):
                    break
                else:
                    print("The value you inputted doesnt match the fields data type\n")

            values.append(value)
        if not self._are_you_happy("with your values", values):
            values = self._get_values(fields, string)

        # the values are in a list but when passing in our values into our sql, they are passed in as a tuple so we convert it into one
        return tuple(values)







    def create_db_file(self):
        # keeps asking the user to create a db file and if it is a db file then we save it 
        self.BACK_DB._close_db()
        
        while True:
            
            db_file = fd.asksaveasfilename(defaultextension = ".db", filetypes = (("database files","*.db"),))
            if  (self.VALID.valid_file(db_file, ".db")):
                #we create aour db file and then close it 
                open(db_file,"w").close()
                sleep(SLEEP_TIME)
                print(f"The Db file {os.path.basename(db_file)} has been created\n")
                break
                
            
          
    def delete_db_file(self):
        # only deletes a db file of your choice
        self.BACK_DB._close_db()
        while True:
            db_path = fd.askopenfilename(title = "Select file",filetypes = [("database files","*.db")])
            if self.VALID.valid_file(db_path, ".db"):

                os.remove(db_path)
                sleep(SLEEP_TIME)
                print(f"Database {os.path.basename(db_path)} has been deleted\n")
                break
        

    def open_db_file(self):
        # opens  a db file and connects to it 
        self.BACK_DB._close_db()
        while True:
            db_path = fd.askopenfilename(title = "Select file",filetypes = [("database files","*.db")])

            if self.VALID.valid_file(db_path, ".db"):
                db_name = os.path.basename(db_path)
                self.BACK_DB._connect_db(db_path,db_name)
                sleep(SLEEP_TIME)
                print("The database has been connected\n")
                break



    def _get_table_name(self):
        while True:
            table_name = input("What is your table name\n")
            if self.VALID.string_check(table_name):
                return table_name 
            else:
                print("Invalid table name\n")



    def create_table(self):
        # we need to check  if the database is connected and there are no existing tables in that database 
        if self.BACK_DB.db != None and self.BACK_DB.connected_table == None:

            fields_dict = {}
            table_name = self._get_table_name()
            num_fields = int(input("How many fields are you going to add to your table\n"))
            field_name_string = "("

            # loop thorugh to get our field names and its data type
            for i in range(1, num_fields+1):
                while True:
                    field_name = input(f"Field {i}: Enter your field name\n")
                    field_type = input(f"Field {i}: Enter the data type for this field\n").upper()
                    # checking if it is a valif fieldname and type 
                    if self.VALID.string_check(field_name) and field_type in self.VALID.DATA_TYPES:
                        break
                    print("You either have an invalid field name or invalid field type or both, try again\n")

                # saving the field name and its datatype as a dict
                fields_dict[field_name] = field_type
                # the creating of our the field names query structure is
                field_name_string += (field_name + " " + field_type + ",")

            query_fields = (field_name_string[:len(field_name_string)-1] + "" + field_name_string[len(field_name_string):]) + ")"
            # remove the  last comma, cant replace like a list as strings are immutable in py
            self.BACK_DB._create_table(table_name, query_fields, fields_dict)
            sleep(SLEEP_TIME)
            print("Your table with your fields has been created\n")
        else:
            print("Either a DB is not connected or you have already have a table in your db, check in the menu\n")





    def update_table(self):
        # this updates the tables name by getting new_table
        if self.BACK_DB.db != None and self.BACK_DB.connected_table != None:
            while True:
                new_table_name = input(f"Enter the {self.BACK_DB.connected_table} table's new name\n")
                if self.VALID.string_check(new_table_name):
                    self.BACK_DB._update_table(new_table_name)
                    sleep(2)
                    print(f"The table has been renamed to {new_table_name}\n")
                    break
                else:
                    print("Invalid table name, try again\n")
        else:
            print("Either a DB is not connected or you dont have a table in your db, check in the menu\n")



        
    def delete_table(self):
        if self.BACK_DB.db != None and self.BACK_DB.connected_table != None:
            while True:
                print("Press 1 to confirm to delete the table\n")
                print("Press 2 to not delete your table\n")
                option = input("which option do you choose\n")
                if self.VALID.num_check(option,False):
                    if int(option) == 1:
                        sleep(SLEEP_TIME)
                        self.BACK_DB._delete_tables()
                    else:
                        sleep(SLEEP_TIME)
                        print("OK, we will not delete your table\n")
                    break         
        else:
            print("Either a DB is not connected or you have dont have a table in your db, check in the menu\n")
    


    def insert_record(self):
         # this will stores our records data
        if self.BACK_DB.db != None and self.BACK_DB.connected_table != None:
            
            # this gets the values  for inserting a record 
            values = self._get_values(self.BACK_DB.fields_dict, "Enter your data for the field")
            empty_values_string = "("+"?,"*len(values)

            
            # to remove the last comma
            empty_values_string = empty_values_string[:len(empty_values_string)-1] + "" + empty_values_string[len(empty_values_string):] + ")"

            # tuples are immutable so we add the data to a list then convert it to a tuple
            self.BACK_DB._insert_records(values, empty_values_string)
            sleep(SLEEP_TIME)
            print("Your record has been inserted\n")
        else:
           print("Either a DB is not connected or you have already have a table in your db, check in the menu\n")



    def update_record(self):
        # this updates records by getting the fields to update, the conditions to update, and the new values that will be replacing the old values

        if self.BACK_DB.db != None and self.BACK_DB.connected_table != None:

            # we gets the fields that the user wants to update
            fields_to_update, fields_to_update_str, empty_fields_str1 = self._which_fields("update the field above")


            # this gets the fields of the conditions 
            condition_fields, condition_fields_str, empty_fields_str2 = self._which_fields("want to make this field part of your condition")[0]

            fields_to_update_str+= f" = {empty_fields_str1}"
            condition_str = self._get_conditions(condition_fields)

            new_values = self._get_values(fields_to_update, "Enter your new value for")
            condition_values = self._get_values(condition_fields, "Enter your condition value for")

            values = (new_values + condition_values)
            self.BACK_DB._update_record(fields_to_update_str, condition_str, values)
            sleep(SLEEP_TIME)
            print("Your record has been updated\n")
        else:
           print("Either a DB is not connected or you have already have a table in your db, check in the menu\n")
        



    def delete_record(self):
        # this deletes the reocord depnding on the condition of what the user said
        if self.BACK_DB.db != None and self.BACK_DB.connected_table != None:
            condition_fields_to_delete = self._which_fields("make this field part of your condition")[0]


            condition_str = self._get_conditions(condition_fields_to_delete)
            values = self._get_values(self.BACK_DB.fields_dict,"Enter your condition value")
            self.BACK_DB._delete_records(condition_str, values)
            sleep(SLEEP_TIME)
            print("Your record has been deleted\n")
        else:
           print("Either a DB is not connected or you have already have a table in your db, check in the menu\n")


        
    def _prettier_records_output(self, fields, records):
        widths = [len(field) for field in fields]
        for record in records:
            for i, data in enumerate(record):
                widths[i] = max(len(str(data)), widths[i])

        # Construct formatted row like before
        formatted_row = ' | '.join('{:%d}' % width for width in widths)
        
        print(formatted_row.format(*fields))
        for row in records:
            sleep(0.25)
            print(formatted_row.format(*row))
            
            
        

    def view_all_records(self):

        fields_to_view_str = self._which_fields("view this field")[1]


        fields_to_view_str = fields_to_view_str.replace("(","")
        fields_to_view_str = fields_to_view_str.replace(")","")


        query = f'SELECT {fields_to_view_str} FROM {self.BACK_DB.connected_table}'
        fields_to_view, records = self.BACK_DB._view_records(query)
        self._prettier_records_output(fields_to_view, records)
        



    def view_specific_records(self):
        # this gets the  fields that needs to be viewed 
        fields_to_view_str = self._which_fields("view this field when viewing your record")[1]
        # we need to remove the brackets at the end  or else the query wont work
        fields_to_view_str = fields_to_view_str.replace("(","")
        fields_to_view_str = fields_to_view_str.replace(")", "")


        # this gets the fields for the conditions
        condition_fields = self._which_fields("make this field part of your condition when viewing your record")[0]
        # this generates our condition string, with our fields and boolean operators
        condition_str = self._get_conditions(condition_fields)
        # this gets our values for each field for our condition
        condition_values = self._get_values(condition_fields, "Enter the value for the specific records you want to see for the field")

        # our query string for viewing specific records with specific fields
        query = f'SELECT {fields_to_view_str} FROM {self.BACK_DB.connected_table} WHERE {condition_str}'
        
        fields, records = self.BACK_DB._view_records(query, condition_values)
        # calls a function that makes the records look nice
        self._prettier_records_output(fields, records)





def main(DB_Handler):

    options_dict = {
                    "create a database":DB_Handler.create_db_file,
                    "open a database":DB_Handler.open_db_file,
                    "delete a database":DB_Handler.delete_db_file,
                    "create a table":DB_Handler.create_table,
                    "update a table's name":DB_Handler.update_table,
                    "delete a table":DB_Handler.delete_table,
                    "insert a record":DB_Handler.insert_record,
                    "update a record":DB_Handler.update_record,
                    "delete a record":DB_Handler.delete_record,
                    "view all records":DB_Handler.view_all_records,
                    "view specific records":DB_Handler.view_specific_records
                    }
    while True:
        sleep(1)
        print(f"Connected Database: {DB_Handler.BACK_DB.db_name}\n")
        sleep(0.25)
        print(f"Current connected Table: {DB_Handler.BACK_DB.connected_table}\n")
        # we store our option and its corresponding fucntion ina dict so any option 
        for i ,(option) in enumerate(options_dict):
            
            print(f"Press option {i+1} to {option}\n")
            sleep(0.125)


        option = input("Which option do you choose\n")
        if DB_Handler.VALID.num_check(option, False) and 1<=int(option)<=len(options_dict):
            list(options_dict.values())[int(option)-1]()

        else:
            print("Invalid option, try again\n")

        



if __name__ == "__main__":
    DB_Handler = FrontEndDB()
    main(DB_Handler)
    