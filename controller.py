import utils as utils


class Controller(object):

    # Very strange and not typical code
    def __init__(self, model, view):
        self.model = model
        self.view = view

    def start(self):
        self.view.print_hello_message()
        self.show_main_menu()

    # Main menu handler
    def show_main_menu(self):
        self.view.print_start_menu()

        input_v = self.view.request_input("Enter number (from 1 to 5):",
                                          valid_cases=['1', '2', '3', '4', '5'])

        if input_v == "1":
            self.print_tables()
            self.show_main_menu()

        if input_v == "2":
            sql_query = self.view.request_input("Enter query:")
            self.view.print_data(self.model.query(sql_query), on_none_message="NOTHING")
            self.show_main_menu()

        if input_v == "3":
            self.find_menu()

        if input_v == "4":
            tables = self.model.list_tables()
            phraze = self.view.request_input("Enter phraze:")
            for table in tables:
                print("On table %s:" % (table,))
                self.view.print_table(self.model.find_by_phraze(table, phraze), "NOTHING")
            self.show_main_menu()

    # Ask user to enter fields values of some object. Return None if problems
    def request_input_object(self, table_name, message="You can enter nothing for random value.", random_on_none=True):
        data_list = []
        print(message)
        for column_data in self.model.get_table_columns_data(table_name):
            data = self.view.request_input("\tField '" + column_data[0] + "'(" + column_data[1] + "):")
            if data == 'back':
                return
            elif random_on_none and data == '':
                data_list.append(utils.gen_random(column_data[1]))
            else:
                data_list.append(data)
        return data_list

    # Select table menu
    def print_tables(self):
        tables = self.model.list_tables()
        self.view.print_tables(tables)
        input_v = self.view.request_input("Enter number (from 1 to " + str(len(tables)) + "):",
                                          validator=lambda x: x.isdigit() and 0 < int(x) <= len(tables))
        if input_v == "back":
            return None
        self.table_menu(tables[int(input_v) - 1])

    # Ask user to select some field of table and expected value on this field(for SELECT's)
    def select_obj_menu(self, table_name):
        columns = self.model.list_columns(table_name)
        self.view.select_column_menu(table_name, columns)
        input_v = self.view.request_input("Enter number (from 1 to " + str(len(columns)) + "):",
                                          validator=lambda x: x.isdigit() and 0 < int(x) <= len(columns))
        if input_v != "back":
            column = columns[int(input_v) - 1]
            expected_value = self.view.request_input("\tEnter expected value on field %s:" % (column,))
            if expected_value != "back":
                return column, expected_value
        return None, None

    # What can you do with table?
    def table_menu(self, table_name):
        self.view.print_table_menu(table_name)
        input_v = self.view.request_input("Enter number (from 1 to 6):",
                                          valid_cases=["1", "2", "3", "4", "5", "6"])

        if input_v != "back":
            # SELECT ALL
            if input_v == "1":
                data = self.model.get_full_table(table_name)
                self.view.print_table(data)
                self.view.after_action_message(data)
                self.table_menu(table_name)

            # DELETE
            if input_v == "2":
                column, value = self.select_obj_menu(table_name)
                if column and value:
                    self.view.after_action_message(self.model.delete_data(table_name, column, value))
                self.table_menu(table_name)

            # INSERT
            if input_v == "3":
                def insert():
                    self.view.after_action_message(self.model.insert_data(table_name,
                                                                          tuple(self.request_input_object(table_name))))

                insert()
                self.table_menu(table_name)

            # UPDATE
            if input_v == "4":
                self.update_menu(table_name)
                self.table_menu(table_name)

            # SELECT
            if input_v == "5":
                column, value = self.select_obj_menu(table_name)
                if column and value:
                    data = self.model.select_some(table_name, column, value)
                    self.view.print_table(data, on_none_message="NOTHING FOUND")
                    self.view.after_action_message(data)
                self.table_menu(table_name)

            # INSERT RANDOM
            if input_v == "6":
                self.view.after_action_message(self.model.insert_random(table_name))
                self.table_menu(table_name)

    # Update menu
    def update_menu(self, table_name):
        print("SELECT OBJECT TO UPDATE:")
        c, v = self.select_obj_menu(table_name)
        if c and v:
            obj = self.request_input_object(table_name, "Enter nothing for not touching field", False)
            if obj:
                self.view.after_action_message(self.model.update(table_name, c, v, obj))


    # TABLE DEPENDENCY ZONE

    # Just find menu
    def find_menu(self):
        self.view.find_menu()
        input_v = self.view.request_input("Enter number (from 1 to 4):",
                                          valid_cases=["1", "2", "3", "4"])
        if input_v != 'back':
            if input_v == '1':
                data = self.view.request_input("Enter 'adblock_using' param(boolean):")
                if data != 'back' and data:
                    data = data.lower()
                    if data != 'true' and data != 'false' and data != 'none' and data != 'null':
                        print(data, "isn't bool")
                    else:
                        val = self.model.find_1((data == 'true') if data == 'true' or data == 'false' else None)
                        self.view.print_table(val, on_none_message="NOTHING FOUND")
                        self.view.after_action_message(val)

            if input_v == '2':
                data = self.view.request_input("Enter word(text):")
                if data != 'back' and data:
                    val = self.model.find_2(data)
                    self.view.print_table(val, on_none_message="NOTHING FOUND")
                    self.view.after_action_message(val)

            if input_v == '3':
                data_s = self.view.request_input("Enter start_time param(timestamp with time zone):")
                if data_s != 'back' and data_s:
                    data_e = self.view.request_input("Enter start_time param(timestamp with time zone):")
                    if data_e != 'back' and data_e:
                        val = self.model.find_3(data_s, data_e)
                        self.view.print_table(val, on_none_message="NOTHING FOUND")
                        self.view.after_action_message(val)

            if input_v == '4':
                data = self.view.request_input("Enter word param(text):")
                if data != 'back' and data:
                    val = self.model.find_4(data)
                    self.view.print_table(val, on_none_message="NOTHING FOUND")
                    self.view.after_action_message(val)

            self.find_menu()
