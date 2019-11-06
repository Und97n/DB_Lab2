from prettytable import PrettyTable
import getch
import sys


class View(object):

    def print_hello_message(self):
        print("Hello. You can always type 'back' and 'exit', even if i don't say that. Enjoy.")

    # start menu handler
    def print_start_menu(self):
        print("\n::::::::::::::::::::::::::::::::::::::::")
        print("\t1: View Tables")
        print("\t2: SQL Query")
        print("\t3: Find String")
        print("\t4: Exit")

    def print_table(self, table_data):
        x = PrettyTable()
        x.field_names = table_data[0]
        for row in table_data[1]:
            x.add_row(row)
        print(x)

    # Very nice looking code
    def request_input(self,
                      message,
                      valid_cases=[],
                      validator=None,
                      message_on_wrong="Wrong input, try again(or enter 'back'):"):
        if validator is None:
            if valid_cases:
                validator = lambda x: (any(x is s for s in valid_cases))
            else:
                validator = lambda x: True

        retval = None
        print(message, end=" ")
        while True:
            retval = input()
            if retval == 'back' or validator(retval):
                return retval
            else:
                if retval == 'exit':
                    print("Bye")
                    sys.exit(0)
                else:
                    print(message_on_wrong, end=" ")

    # друкує меню з таблицями
    def print_tables(self, tables_list):
        counter = 1
        for table in tables_list:
            print("\t", counter, ": ", table, sep="")
            counter += 1

    def print_and_getch(self, message):
        print(message)
        return getch.getch()

    def after_action_message(self, is_all_ok):
        return self.print_and_getch(("Ok." if is_all_ok else "FAIL."))

    def print_table_menu(self, table_name):
        print("TABLE:", table_name)
        print("\t1: SELECT ALL")
        print("\t2: DELETE")
        print("\t3: INSERT")
        print("\t4: UPDATE")
        print("\t5: SELECT")
        print("\t6: INSERT RANDOM")
        print("\t7: FIND")
    #
    # # друкує find меню для таблиці
    # def find_menu(self, table_name):
    #     if table_name == constants.author_table:
    #         print("1. FIND ALL AUTHOR BOOKS")
    #         print("2. FIND ALL READERS THAT READING AUTHOR BOOKS")
    #         print("3. FIND READER'S PHONES THAT READ AUTHOR BOOKS")
    #         print()
    #         print("4. Back")
    #         return
    #     if table_name == constants.reader_table:
    #         print("1. FIND ALL READERS WITH PREMIUM SUBSCRIPTION")
    #         print("2. FIND ALL READERS WITH SUBSCRIPTION WITH PARTICULAR DATE")
    #         print("3. FIND ALL BOOKS THAT REDEAR READ")
    #         print()
    #         print("4. Back")
    #         return
    #     if table_name == constants.book_table:
    #         print("1. FIND ALL READERS THAT READ BOOK")
    #         print("2. FIND ALL AUTHORS THAT WROTE BOOK")
    #         print("3. FIND ALL READERS THAT READ AND WITH PARTICULAR SUBSCRIPTION")
    #         print()
    #         print("4. Back")
    #         return
    #     print("1. Back")
    #
    # # друкує атрибути об'єкта
    # def print_object_keys_menu(self, object_keys):
    #     index = 0
    #     for object_key in object_keys:
    #         index += 1
    #         print(str(index) + ". " + str(object_key))
    #
    #     print()
    #     print(str(index + 1) + ". Back")
    #
    # # запит на ввод об'єкта користувачем
    # def request_input_object(self, obj, full_input = False, formating = True):
    #     index = 0
    #     new_obj = {}
    #     for key in obj.keys():
    #         if not full_input and index == 0:
    #             index += 1
    #             continue
    #
    #         print(key + " = ")
    #         key_input = self.request_input("", True)
    #         if formating:
    #             new_obj[key] = self.fromat_key(key_input, obj[key])
    #         else:
    #             new_obj[key] = key_input
    #     return new_obj
    #
    # # TODO FIX IT!!!
    # # формування дефотлних значень для об'єкта (для майбутньої валідації)
    # def fromat_key(self, key, key_type):
    #     if key_type == 'integer':
    #         try:
    #             return int(key)
    #         except ValueError:
    #             return None
    #     if key_type == 'text':
    #         return "'" + str(key) + "'"
    #     if key_type == 'timestamp':
    #         return "'" + str(key) + "'"
    #     if key_type == 'bool':
    #        if key == '':
    #            return None
    #        else:
    #            return key
    #
