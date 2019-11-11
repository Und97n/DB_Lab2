import utils as utils
import psycopg2
from psycopg2 import sql


class Model(object):

    def __init__(self, host, password):
        self.open_connection = lambda: utils.open_connection(host, 5432, "postgres", "postgres", password)

    # Select some from some table
    def select_some(self, table_name, column, value):
        with self.open_connection() as conn:
            with conn.cursor() as cursor:
                data = utils.query(cursor, sql.SQL("""
                        SELECT * FROM {} WHERE {}=%s;
                        """).format(sql.Identifier(table_name), sql.Identifier(column)), (value,))
                if data:
                    return [utils.list_table_columns(cursor, table_name), data]

    # Update some in some table
    # Details in 'utils'
    def update(self, table_name, column_to_check, exp_value, new_data):
        with self.open_connection() as conn:
            with conn.cursor() as cursor:
                return utils.update_item(conn, cursor, table_name, column_to_check, exp_value, new_data)

    # Search phraze in all text columns of table
    def find_by_phraze(self, table_name, phraze):
        with self.open_connection() as conn:
            with conn.cursor() as cursor:
                def find_by_phraze(column):
                    return val

                columns = utils.list_table_columns(cursor, table_name)
                columns = list(filter((lambda x: utils.get_column_type(cursor, table_name, x) == 'text'), columns))
                data = []
                for column in columns:
                    val = utils.query(cursor, sql.SQL("""
                    SELECT * FROM {} WHERE {} LIKE %s;
                    """).format(sql.Identifier(table_name), sql.Identifier(column)),
                      ("%{}%".format(phraze),))
                    if val:
                        data.extend(val)
                if data:
                    return [utils.list_table_columns(cursor, table_name), list(dict.fromkeys(data))]

    # Look in 'utils'
    def list_tables(self):
        with self.open_connection() as conn:
            with conn.cursor() as cursor:
                return utils.list_tables(cursor)

    # Look in 'utils'
    def list_columns(self, table_name):
        with self.open_connection() as conn:
            with conn.cursor() as cursor:
                return utils.list_table_columns(cursor, table_name)

    # Get full table from database.
    def get_full_table(self, table_name):
        with self.open_connection() as conn:
            with conn.cursor() as cursor:
                columns = utils.list_table_columns(cursor, table_name)
                data = utils.query(cursor, sql.SQL("""
                    SELECT * FROM {};
                    """).format(sql.Identifier(table_name)), ())

                if columns and data:
                    return [columns, data]

    # Insert some random value to some table.
    def insert_random(self, table_name):
        with self.open_connection() as connection:
            with connection.cursor() as cursor:
                def gen_rand_data(x):
                    return utils.gen_random(utils.get_column_type(cursor, table_name, x))

                random_data = tuple(gen_rand_data(x) for x in (utils.list_table_columns(cursor, table_name)))
                return utils.insert_data(connection, cursor, table_name, random_data)

    # Get column data from table.
    # Returns list of tuples, where first element is column name and second - type of column
    def get_table_columns_data(self, table_name):
        with self.open_connection() as connection:
            with connection.cursor() as cursor:
                columns = utils.list_table_columns(cursor, table_name)
                return list(zip(columns, map((lambda x: utils.get_column_type(cursor, table_name, x)), columns)))

    # Insert some data to some table
    # Details in 'utils'
    def insert_data(self, table_name, data):
        with self.open_connection() as connection:
            with connection.cursor() as cursor:
                return utils.insert_data(connection, cursor, table_name, data)

    # Delete some data in database.
    # Details in 'utils'
    def delete_data(self, table_name, column_name, expected_value):
        with self.open_connection() as connection:
            with connection.cursor() as cursor:
                return utils.delete_data(connection, cursor, table_name, column_name, expected_value)

    # Details in 'utils'
    def query(self, q):
        with self.open_connection() as connection:
            with connection.cursor() as cursor:
                return utils.query(cursor, q, ())

    # TABLE DEPENDENCY ZONE

    # Find all users by using/not-using adblock in last session
    def find_1(self, adblock_using):
        with self.open_connection() as connection:
            with connection.cursor() as cursor:
                data = utils.query(cursor, """
                SELECT "user".* FROM "user" 
                JOIN "session" ON us_last_session=ss_id 
                WHERE ss_with_adblock IS %s;
                """, (adblock_using,))
                if data:
                    return [utils.list_table_columns(cursor, 'user'), data]

    # Find themes, where connected product contains in name some word.
    def find_2(self, prd_name_contains):
        with self.open_connection() as connection:
            with connection.cursor() as cursor:
                data = utils.query(cursor, """
                SELECT theme.* FROM theme 
                JOIN ad ON ad_theme=th_id 
                JOIN product ON ad_product=prd_id
                WHERE to_tsvector(prd_name) @@ to_tsquery(%s)
                GROUP BY th_id;
                """, (prd_name_contains,))
                if data:
                    return [utils.list_table_columns(cursor, 'theme'), data]

    # Find users with last session in time between two timestamps
    def find_3(self, start_time, end_time):
        with self.open_connection() as connection:
            with connection.cursor() as cursor:
                data = utils.query(cursor, """
                SELECT "user".* FROM "user" 
                JOIN "session" ON us_last_session=ss_id 
                WHERE
                    ss_start_time > %s AND
                    ss_end_time < %s;
                """, (start_time, end_time))
                if data:
                    return [utils.list_table_columns(cursor, 'user'), data]

    # Find all ads, promoter of that does not contains some word in registration place(country, for example)
    def find_4(self, not_contains_word):
        with self.open_connection() as connection:
            with connection.cursor() as cursor:
                data = utils.query(cursor, """
                SELECT ad.* FROM ad 
                JOIN promoter ON ad_promoter=pr_id 
                WHERE NOT (to_tsvector(pr_regplace) @@ to_tsquery(%s));
                """, (not_contains_word, ))
                if data:
                    return [utils.list_table_columns(cursor, 'ad'), data]
