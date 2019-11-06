import utils as utils


class Model(object):

    def __init__(self, host, password):
        self.connection = utils.open_connection(host, 5432, "postgres", "postgres", password)
        self.cursor = self.connection.cursor()

    def select_all(self, table_name):
        return utils.select_all(self.cursor, table_name)

    def list_tables(self):
        return utils.list_tables(self.cursor)

    def get_full_table(self, table_name):
        return utils.get_full_table(self.cursor, table_name)

    def insert_random(self, table_name):
        def gen_rand_data(x):
            return utils.gen_random(utils.get_column_type(self.cursor, table_name, x))
        random_data = tuple(gen_rand_data(x) for x in (utils.list_table_columns(self.cursor, table_name)))
        print(random_data)
        return utils.insert_data(self.connection, self.cursor, table_name, random_data)

    def delete_data(self, table_name, cond_string):
        return utils.delete_data(self.connection, self.cursor, table_name, cond_string)

