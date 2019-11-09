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
            print(self.model.query(sql_query))
            self.show_main_menu()
        #
        # if input == "3":
        #     string = self.view.request_input("String to find: ")
        #     self.model.find_no_string_in_all_tables(string)

        if input_v == "4":
            utils.do_nothing()

        if input_v == "back":
            utils.do_nothing()
            self.show_main_menu()

    # handler меню таблиць
    def print_tables(self):
        tables = self.model.list_tables()
        self.view.print_tables(tables)
        input_v = self.view.request_input("Enter number (from 1 to " + str(len(tables)) + "):",
                                          validator=lambda x: 0 < int(x) <= len(tables))
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
                                          valid_cases=["1", "2", "3", "4", "5", "6", "7"])

        if input_v != "back":
            # SELECT ALL
            if input_v == "1":
                models = self.model.select_all(table_name)
                self.view.print_table(self.model.get_full_table(table_name))
                self.view.print_and_getch("")
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
                    for column_data in self.model.get_table_columns_data(table_name):
                        data = self.view.request_input("\tField '" + column_data[0] + "'(" + column_data[1] + "):")
                        if data != 'back':
                            data_list.append(data)
                        else:
                            return
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
                    self.view.print_table(data, "NOTHING FOUND")
                    self.view.after_action_message(data)
                self.table_menu(table_name)

            # INSERT RANDOM
            if input_v == "6":
                self.view.after_action_message(self.insert_random(table_name))
                self.table_menu(table_name)

            #FIND
            # if input == "7":
            #     self.find_menu(table_name)

    # handler random insert
    def insert_random(self, table_name):
        self.model.insert_random(table_name)

    # # handler find
    # def find_menu(self, table_name):
    #     self.view.find_menu(table_name)
    #
    #     if table_name == constants.book_table or table_name == constants.author_table or table_name == constants.reader_table:
    #         input = self.view.request_input("Enter number (from 1 to 4)")
    #         is_valid = validate_input(input, ["1","2","3","4"])
    #
    #         if is_valid:
    #             if table_name == constants.reader_table:
    #                 self.reader_find_menu(input)
    #
    #             if table_name == constants.book_table:
    #                 self.book_find_menu(input)
    #
    #             if table_name == constants.author_table:
    #                 self.author_find_menu(input)
    #
    #             self.table_controller(table_name)
    #
    #     else:
    #         input = self.view.request_input("", True)
    #         is_valid = validate_input(input, ["1"])
    #         if is_valid:
    #             self.table_controller(table_name)

    # # find handler для таблиці reader
    # def reader_find_menu(self, input):
    #     if input == "3":
    #         r_name = self.view.request_input("Reader name")
    #         self.model.find_query(constants.reader_table, input, {"r_name": r_name})
    #
    #     if input == "2":
    #         subscriptio_object = {"s_premium": False, "s_date": ''}
    #         self.view.print_message("Object to select:")
    #         obj = self.view.request_input_object(subscriptio_object, full_input=True, formating=False)
    #         self.model.find_query(constants.reader_table, input, obj)
    #
    #     if input == "1":
    #         subscriptio_object = {"s_premium": False}
    #         self.view.print_message("Object to select:")
    #         obj = self.view.request_input_object(subscriptio_object, full_input=True, formating=False)
    #         self.model.find_query(constants.reader_table, input, obj)
    #
    #     self.find_menu(constants.reader_table)
    #
    # # select handler для таблиці
    # def select_menu(self, table_name):
    #     def_obj = self.model.get_object(table_name)
    #     self.view.print_message("Object to select:")
    #     obj = self.view.request_input_object(def_obj, True)
    #     object_to_find = get_formatted_object(obj)
    #     print(self.model.select_item(table_name, object_to_find))
    #
    # # update handler для таблиці
    # def update_menu(self, table_name):
    #     def_obj = self.model.get_object(table_name)
    #     self.view.print_message("Object to update:")
    #     obj = self.view.request_input_object(def_obj, True)
    #     object_to_find = get_formatted_object(obj)
    #     print("#Need to update: " + str(object_to_find))
    #     print("Def obj: " + str(def_obj))
    #     new_object = self.view.request_input_object(def_obj)
    #     print(new_object)
    #     new_object = get_formatted_object(new_object)
    #     print(str(new_object))
    #     self.model.update_item(table_name, object_to_find, new_object)
    #
    # # delete handler для таблиці
    # def delete_menu(self, table_name):
    #     obj = self.model.get_object(table_name)
    #     obj = self.view.request_input_object(obj, True)
    #     self.view.print_message(obj)
    #     object_to_find = get_formatted_object(obj)
    #     print("#Need to delete: " + str(object_to_find))
    #     self.model.delete_item(table_name, object_to_find)
    #
    # # insert handler для таблиці
    # def insert_menu(self, table_name):
    #     obj = self.model.get_object(table_name)
    #     obj = self.view.request_input_object(obj)
    #     print("#Added: " + str(self.model.insert_item(obj, table_name)))
    #
    # # select all  handler для таблиці
    # def select_all(self, table_name):
    #     items = self.model.select_all(table_name)
    #     return items