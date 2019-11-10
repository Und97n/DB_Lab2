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

        input_v = self.view.request_input("Enter number (from 1 to 4)",
                                          valid_cases=['1', '2', '3', '4'])

        if input_v == "1":
            self.print_tables()
            self.show_main_menu()

        if input_v == "2":
            sql_query = self.view.request_input("Enter query:")
            self.view.print_data(self.model.query(sql_query), on_none_message="NOTHING")
            self.show_main_menu()

        if input_v == "3":
            self.find_menu()

    # handler меню таблиць
    def print_tables(self):
        tables = self.model.list_tables()
        self.view.print_tables(tables)
        input_v = self.view.request_input("Enter number (from 1 to " + str(len(tables)) + "):",
                                          validator=lambda x: x.isdigit() and 0 < int(x) <= len(tables))
        if input_v == "back":
            return None
        self.table_menu(tables[int(input_v)-1])

    def select_obj_menu(self):
        column = self.view.request_input("\tEnter field to check:")
        if column != "back" and column != "":
            expected_value = self.view.request_input("\tEnter expected value on this field:")
            if expected_value != "back":
                return column, expected_value
        return None, None

    def table_menu(self, table_name):
        self.view.print_table_menu(table_name)
        input_v = self.view.request_input("Enter number (from 1 to 7):",
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
                column, value = self.select_obj_menu()
                if column and value:
                    self.view.after_action_message(self.model.delete_data(table_name, column, value))
                self.table_menu(table_name)

            # INSERT
            if input_v == "3":
                def insert():
                    data_list = []
                    print("You can enter nothing for random value.")
                    for column_data in self.model.get_table_columns_data(table_name):
                        data = self.view.request_input("\tField '" + column_data[0] + "'(" + column_data[1] + "):")
                        if data == 'back':
                            return
                        elif data == '':
                            data_list.append(utils.gen_random(column_data[1]))
                        else:
                            data_list.append(data)

                    self.view.after_action_message(self.model.insert_data(table_name, tuple(data_list)))
                insert()
                self.table_menu(table_name)

            # # UPDATE
            # if input_v == "4":
            #     self.update_menu(table_name)
            #     self.view.print_divider(2)
            #     self.table_controller(table_name)
            #
            # SELECT
            if input_v == "5":
                column, value = self.select_obj_menu()
                if column and value:
                    data = self.model.select_some(table_name, column, value)
                    self.view.print_table(data, on_none_message="NOTHING FOUND")
                    self.view.after_action_message(data)
                self.table_menu(table_name)

            # INSERT RANDOM
            if input_v == "6":
                self.view.after_action_message(self.model.insert_random(table_name))
                self.table_menu(table_name)

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

    # update handler для таблиці
    def update_menu(self, table_name):
        def_obj = self.model.get_object(table_name)
        self.view.print_message("Object to update:")
        obj = self.view.request_input_object(def_obj, True)
        object_to_find = get_formatted_object(obj)
        print("#Need to update: " + str(object_to_find))
        print("Def obj: " + str(def_obj))
        new_object = self.view.request_input_object(def_obj)
        print(new_object)
        new_object = get_formatted_object(new_object)
        print(str(new_object))
        self.model.update_item(table_name, object_to_find, new_object)
