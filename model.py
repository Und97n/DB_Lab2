import utils as utils
import psycopg2
from psycopg2 import sql


class Model(object):

    def __init__(self, host, password):
        self.open_connection = lambda: utils.open_connection(host, 5432, "postgres", "postgres", password)

    def select_some(self, table_name, column, value):
        with self.open_connection() as conn:
            with conn.cursor() as cursor:
                data = utils.query(cursor, sql.SQL("""
                        SELECT * FROM {} WHERE {}=%s;
                        """).format(sql.Identifier(table_name), sql.Identifier(column)), (value,))
                if data:
                    return [utils.list_table_columns(cursor, table_name), data]

    def list_tables(self):
        with self.open_connection() as conn:
            with conn.cursor() as cursor:
                return utils.list_tables(cursor)

    def get_full_table(self, table_name):
        with self.open_connection() as conn:
            with conn.cursor() as cursor:
                columns = utils.list_table_columns(cursor, table_name)
                data = utils.query(cursor, sql.SQL("""
                    SELECT * FROM {};
                    """).format(sql.Identifier(table_name)), ())

                if columns and data:
                    return [columns, data]

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

    def query(self, q):
        with self.open_connection() as connection:
            with connection.cursor() as cursor:
                return utils.query(cursor, q, ())

    # TABLE DEPENDENCY ZONE

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

    def find_2(self, prd_name_contains):
        with self.open_connection() as connection:
            with connection.cursor() as cursor:
                data = utils.query(cursor, """
                SELECT theme.* FROM theme 
                JOIN ad ON ad_theme=th_id 
                JOIN product ON ad_product=prd_id
                WHERE prd_name @@ %s
                GROUP BY th_id;
                """, (prd_name_contains,))
                if data:
                    return [utils.list_table_columns(cursor, 'theme'), data]

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

    def find_4(self, not_contains_word):
        with self.open_connection() as connection:
            with connection.cursor() as cursor:
                data = utils.query(cursor, """
                SELECT ad.* FROM ad 
                JOIN promoter ON ad_promoter=pr_id 
                WHERE NOT (pr_regplace @@ %s);
                """, (not_contains_word, ))
                if data:
                    return [utils.list_table_columns(cursor, 'ad'), data]
