# The main function provides a commandline interface for the package.
# This way you can use it via python -m modulename.

from pycsvtosqliteroh import *
import argparse

def main():
    """Parameter declaration."""
    # Declaring parameters.
    parser = argparse.ArgumentParser()
    arggroup = parser.add_argument_group(title="CsvToSqlite")
    arggroup.add_argument("-file", "--file", type=str, help=("Csv file that will be converted."))
    arggroup.add_argument("-db", "--database", type=str, help=("Sqlite database."))
    arggroup.add_argument("-table", "--tablename", type=str, help=("Sqlite table."))

    args = parser.parse_args()

    # Catchin parameters.
    if args.file and args.database and not args.tablename:
        csvobj = CsvToSqlite(args.file, args.database)
        csvobj.create_table_from_csv()
    elif args.file and args.database and args.tablename:
        sqliteobj = SqliteToCsv(args.database, args.file, args.tablename)
        sqliteobj.convert_table_to_csv()
    else:
        raise ValueError("Provided input is not correct. Specify a .csv file and a sqlite database.")

if __name__ == '__main__':
    main()