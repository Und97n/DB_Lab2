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


def close_connection(connection, cursor):
    if connection is not None:
        cursor.close()
        connection.close()
        print("З'єднання з PostgreSQL закрите")


def list_tables(cursor):
    cursor.execute("""
    SELECT table_name FROM information_schema.tables 
    WHERE table_schema = 'public';
    """)
    retval = cursor.fetchall()
    return [x[0] for x in retval]


def list_table_columns(cursor, table):
    cursor.execute("""
    SELECT column_name
    FROM information_schema.columns
    WHERE table_schema = 'public'
        AND table_name = %s;
    """, (table,))
    retval = cursor.fetchall()
    return [x[0] for x in retval]


def get_column_type(cursor, table, column):
    cursor.execute("""
    SELECT data_type
    FROM information_schema.columns
    WHERE table_schema = 'public'
        AND table_name = %s
        AND column_name = %s;
    """, (table, column))
    retval = cursor.fetchall()
    if retval:
        return retval[0][0]
    else:
        return None


def select_all(cursor, table):
    query = sql.SQL("""
        SELECT * FROM {};
        """).format(sql.Identifier(table))

    cursor.execute(query)
    retval = cursor.fetchall()
    if retval:
        return retval[0][0]
    else:
        return None


def select_some(cursor, table, column_to_check, expected_column_value):
    query = sql.SQL("""
        SELECT * FROM {} WHERE {}=%s;
        """).format(sql.Identifier(table), sql.Identifier(column_to_check))

    try:
        cursor.execute(query, (expected_column_value))
        retval = cursor.fetchall()

        if retval:
            return retval[0][0]
        else:
            return None
    except BaseException as e:
        print("ERROR: ", str(e))
        return False


# Insert some data to table. NO TYPE CHECKS!!!
def insert_data(connection, cursor, table, data):
    query = sql.SQL("""
        INSERT INTO {} VALUES %s;
        """).format(sql.Identifier(table))

    try:
        cursor.execute(query, (data,))
        connection.commit()
    except BaseException as e:
        print("ERROR: ", str(e))
        return False
    return True


# Insert some data to table. NO CHECKS!!!
def delete_data(connection, cursor, table, column_name, expected_value):
    query = sql.SQL("""
        DELETE FROM {} WHERE {}=%s;
        """).format(sql.Identifier(table), sql.Identifier(column_name))

    try:
        cursor.execute(query, (expected_value,))
        connection.commit()
    except BaseException as e:
        print("ERROR: ", str(e))
        return False
    return True


def get_full_table(cursor, table):
    columns = list_table_columns(cursor, table)
    query = sql.SQL("""
    SELECT * FROM {};
    """).format(sql.Identifier(table))

    cursor.execute(query)
    table = cursor.fetchall()
    return [columns, table]


def random_string():
    random_str = ""
    for i in range(0, random.randint(0, 30)):
        random_str += str(random.choice("0123456789abcdefghijklmnopqrstuvwxyz"))
    return random_str


# Unknown type => None
def gen_random(type_v):
    switcher = {
        'integer': lambda: random.randint(0, 16387),
        'text': lambda: random_string(),
    }
    return (switcher.get(type_v, lambda: None))()


# Do nothing
def do_nothing():
    return None  # do nothing
