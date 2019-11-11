import psycopg2
import random
from psycopg2 import sql


def open_connection(phost, pport, pdatabase, puser, ppassword):
    try:
        return psycopg2.connect(host=phost, port=pport, database=pdatabase, user=puser, password=ppassword)
    except (Exception, psycopg2.Error) as error:
        print("Error: connection with PostgreSQL\n\t", error)


def get_cursor(connection):
    return connection.cursor()


def query(cursor, q, query_params):
    try:
        cursor.execute(q, query_params)
        retval = cursor.fetchall()
        if retval:
            return retval
    except BaseException as e:
        print("ERROR: ", str(e))


def list_tables(cursor):
    data = query(cursor, """
    SELECT table_name FROM information_schema.tables 
    WHERE table_schema = 'public';
    """, ())
    if data:
        return [x[0] for x in data]


def list_table_columns(cursor, table):
    data = query(cursor, """
    SELECT column_name
    FROM information_schema.columns
    WHERE table_schema = 'public'
        AND table_name = %s;
    """, (table,))
    if data:
        return [x[0] for x in data]


def get_column_type(cursor, table, column):
    data = query(cursor, """
    SELECT data_type
    FROM information_schema.columns
    WHERE table_schema = 'public'
        AND table_name = %s
        AND column_name = %s;
    """, (table, column))
    if data:
        return data[0][0]


# Insert some data to table. NO TYPE CHECKS!!!
def insert_data(connection, cursor, table, data):
    q = sql.SQL("""
        INSERT INTO {} VALUES %s;
        """).format(sql.Identifier(table))

    try:
        cursor.execute(q, (data,))
        connection.commit()
    except BaseException as e:
        print("ERROR: ", str(e))
        return False
    return True


def update_item(connection, cursor, table_name, column_to_check, expected_value, new_data):
    columns = list_table_columns(cursor, table_name)
    insert_str = ""
    for i in range(0, len(columns)):
        # '' means default value
        if new_data[i] != '':
            if insert_str != "":
                insert_str += ', '
            insert_str += "%s='%s'" % (columns[i], new_data[i])

    q = sql.SQL("""
    UPDATE {} SET """ + insert_str + """ WHERE {}=%s;
    """).format(sql.Identifier(table_name), sql.Identifier(column_to_check))

    try:
        cursor.execute(q, (expected_value, ))
        connection.commit()
    except BaseException as e:
        print("ERROR: ", str(e))
        return False
    return True


# Insert some data to table. NO CHECKS!!!
def delete_data(connection, cursor, table, column_name, expected_value):
    q = sql.SQL("""
        DELETE FROM {} WHERE {}=%s;
        """).format(sql.Identifier(table), sql.Identifier(column_name))

    try:
        cursor.execute(q, (expected_value,))
        connection.commit()
    except BaseException as e:
        print("ERROR: ", str(e))
        return False
    return True


def random_string():
    random_str = ""
    for i in range(0, random.randint(5, 10)):
        random_str += str(random.choice("0123456789abcdefghijklmnopqrstuvwxyz"))
    return random_str


# Unknown type => None
def gen_random(type_v):
    switcher = {
        'integer':
            lambda: random.randint(0, 16387),
        'text':
            lambda: random_string(),
        'bigint':
            lambda: random.randint(0, 16387),
        'boolean':
            lambda: random.choice(['true', 'false']),
        'timestamp with time zone':
            # 2019-08-21 08:30:00+03:00
            lambda: "%04d-%02d-%02d %02d:%02d:%02d+%02d:00" %
                    (random.randint(1970, 2037),  # year
                     random.randint(1, 12),  # month
                     random.randint(1, 28),  # day
                     random.randint(0, 23),  # hour
                     random.randint(0, 59),  # minute
                     random.randint(0, 59),  # second
                     random.randint(0, 11),  # timezone
                     ),
    }
    return (switcher.get(type_v, lambda: None))()


# Do nothing
def do_nothing():
    return None  # do nothing
