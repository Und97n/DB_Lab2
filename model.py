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
        random_item = randomizer.generate_random_item(database_helper.get_table_object(table_name))
        result = database_helper.insert_item(connection, cursor, table_name, random_item)
        database_helper.close_database_connection(connection, cursor)
        return result

