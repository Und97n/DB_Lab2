from prettytable import PrettyTable
import getch
import sys


class View(object):

    # This message is displayed on program start
    def print_hello_message(self):
        print("Hello. You can always type 'back' and 'exit', even if i don't say that. Enjoy.")

    # Print start menu entries
    def print_start_menu(self):
        print("\n::::::::::::::::::::::::::::::::::::::::")
        print("\t1: View Tables")
        print("\t2: SQL Query")
        print("\t3: Find some")
        print("\t4: Find in all tables by phraze")
        print("\t5: Exit")

    # Print some data. Data - list of tuples(table). No columns names specified.
    def print_data(self, table_data, on_none_message=None):
        if table_data:
            x = PrettyTable()
            for row in table_data:
                x.add_row(row)
            print(x)
        elif on_none_message:
            print(on_none_message)

    # Print menu entries for selection of some column from column list
    def select_column_menu(self, table_name, columns):
        print("Select some field of table '", table_name, "':", sep="")
        counter = 1
        for column in columns:
            print("\t%d: %s" % (counter, column))
            counter += 1

    # Like print data, but with printing column names. There are in first element of 'table_data'
    def print_table(self, table_data, on_none_message=None):
        if table_data:
            x = PrettyTable()
            x.field_names = table_data[0]

            for row in table_data[1]:
                x.add_row(row)
            print(x)
        elif on_none_message:
            print(on_none_message)

    # Request some input from user. Validation can be done with list of valid cases or with lambda.
    # 'back' and 'exit' are allways valid.
    # 'exit' means exit from program
    # Very nice looking code
    def request_input(self,
                      message,
                      valid_cases=[],
                      validator=None,
                      message_on_wrong="Wrong input, try again(or enter 'back'):"):
        if validator is None:
            validator = (lambda x: (any(x is s for s in valid_cases))) if valid_cases else (lambda _: True)

        print(message, end=" ")
        while True:
            try:
                retval = input()
                if retval == 'back' or validator(retval):
                    return retval
                else:
                    if retval == 'exit':
                        print("Bye")
                        sys.exit(0)
                    else:
                        print(message_on_wrong, end=" ")
            except KeyboardInterrupt:
                print("\nInterrupted by user")
                sys.exit()
            except Exception as e:
                print("Error on input:", e)

    # Print tables list (menu entries)
    def print_tables(self, tables_list):
        counter = 1
        for table in tables_list:
            print("\t", counter, ": ", table, sep="")
            counter += 1

    # Print some message and call 'getch'.
    # User may have some time to rest before menu loop will continue.
    def print_and_getch(self, message):
        print(message)
        return getch.getch()

    # Print Ok if 'is_all_ok', else print 'FAIL'
    # Then call 'getch'
    def after_action_message(self, is_all_ok):
        return self.print_and_getch("Ok" if is_all_ok else "FAIL")

    # Print table actions menu entries
    def print_table_menu(self, table_name):
        print("TABLE:", table_name)
        print("\t1: Select all")
        print("\t2: Delete")
        print("\t3: Insert")
        print("\t4: Update")
        print("\t5: Select where")
        print("\t6: Insert random data")
        print("\t7: Find")

    # Print find menu entries
    def find_menu(self):
        print("FIND MENU")
        print("\t1: Users, who used/not-used adblock at last session")
        print("\t2: Themes, that are connected with product, that contains word in name")
        print("\t3: Users, who have last session in time period")
        print("\t4: Ads, whose promotes don't have word in registration place")
