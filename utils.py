import psycopg2
from psycopg2 import sql
from prettytable import PrettyTable


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


# Insert some data to table. NO TYPE CHECKS!!!
def insert_data(connection, cursor, table, data, columns=None):
    if columns is None:
        columns = list_table_columns(cursor, table)

    query = sql.SQL("""
        INSERT INTO {} %s VALUES %s;
        """).format(sql.Identifier(table))
    try:
        cursor.execute(query, columns, data)
        connection.commit()
    except BaseException as e:
        print(str(e))


def pprint(table_data):
    x = PrettyTable()
    x.field_names = table_data[0]
    for row in table_data[1]:
        x.add_row(row)
    print(x)


def get_full_table(cursor, table):
    columns = list_table_columns(cursor, table)
    query = sql.SQL("""
    SELECT * FROM {};
    """).format(sql.Identifier(table))

    cursor.execute(query)
    table = cursor.fetchall()
    return [columns, table]


def gen_random(type):
    return {
        'integer'
    }[type]


def do_nothing():
    return None
