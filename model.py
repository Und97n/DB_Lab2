import utils as utils
import psycopg2


class Model(object):

    def __init__(self, host, password):
        self.open_connection = lambda: utils.open_connection(host, 5432, "postgres", "postgres", password)

    def select_all(self, table_name):
        with self.open_connection() as conn:
            with conn.cursor() as cursor:
                return utils.select_all(cursor, table_name)

    def list_tables(self):
        with self.open_connection() as conn:
            with conn.cursor() as cursor:
                return utils.list_tables(cursor)

    def get_full_table(self, table_name):
        with self.open_connection() as conn:
            with conn.cursor() as cursor:
                return utils.get_full_table(cursor, table_name)

    def insert_random(self, table_name):
        with self.open_connection() as connection:
            with connection.cursor() as cursor:
                def gen_rand_data(x):
                    return utils.gen_random(utils.get_column_type(cursor, table_name, x))
                random_data = tuple(gen_rand_data(x) for x in (utils.list_table_columns(cursor, table_name)))
                return utils.insert_data(connection, cursor, table_name, random_data)

    def get_table_columns_data(self, table_name):
        with self.open_connection() as connection:
            with connection.cursor() as cursor:
                columns = utils.list_table_columns(cursor, table_name)
                return list(zip(columns, map((lambda x: utils.get_column_type(cursor, table_name, x)), columns)))

    def insert_data(self, table_name, data):
        with self.open_connection() as connection:
            with connection.cursor() as cursor:
                return utils.insert_data(connection, cursor, table_name, data)

    def delete_data(self, table_name, column_name, expected_value):
        with self.open_connection() as connection:
            with connection.cursor() as cursor:
                return utils.delete_data(connection, cursor, table_name, column_name, expected_value)

