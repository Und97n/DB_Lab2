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
            utils.gen_random(utils.get_column_type(self.cursor, table_name, x))
        random_data = map(gen_rand_data, (utils.list_table_columns(self.cursor, table_name)))
        return utils.insert_data(self.connection, self.cursor, table_name, random_data)

