import utils


def main():
    connection = utils.open_connection("127.0.0.1", 5432, "postgres", "postgres", "1")
    cur = connection.cursor()

    for table in utils.list_tables(cur):
        utils.print_table(cur, table)


if __name__ == '__main__':
    main()
