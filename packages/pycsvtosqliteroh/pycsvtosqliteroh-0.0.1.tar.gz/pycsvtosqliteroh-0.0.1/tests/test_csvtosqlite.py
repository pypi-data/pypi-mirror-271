"""Testing the module with the python internal unittest module."""

# Import necessary modules.
import unittest
import os
import sqlite3
# User defined modules.
from src.pycsvtosqliteroh import CsvToSqlite
from src.pycsvtosqliteroh import _Database
from addimportdir import importdir,removedir
from pathlib import Path

# Add current path to PYTHONPATH.
importdir()

# Get all testfiles.
def get_testfiles(dir: str):
    file_list = []
    for file in os.listdir(dir):
        if os.path.isfile(os.path.join(dir, file)):
            file_list.append(os.path.join(dir, file))
    return file_list

# Get filenames without extension to check if tables are created.
def filenames_no_extension(dir: str):
    filelist_no_extension = []
    for file in os.listdir(dir):
        filelist_no_extension.append(Path(file).stem)
    return filelist_no_extension

# Testing main functions.
class TestPycsvtosqliteroh_csvtosqlite(unittest.TestCase):
    
    def setUp(self):
        self.path = "./tests/testfiles"
        self.file_list = get_testfiles(self.path)
        self.database = "./Test.sqlite"

    def test_create_table_from_csv(self):
        for file in self.file_list:
            csvobj = CsvToSqlite(file, self.database)
            csvobj.create_table_from_csv() 
        
    def test_if_table_created(self):
        
        files = filenames_no_extension(self.path)
        # Connect to database and create cursor.
        with _Database(self.database) as db:
            # Get all existing tables.
            queryresult = db.cursor.execute("SELECT name FROM sqlite_master")
            result = queryresult.fetchall()

            # Format result. Result is returned as a list of tuples. [(x,),(y,)]
            # Extracting only the values.
            resultvalues = []
            for value in result:
                resultvalues.append(value[0])
            
            self.assertEqual(files, resultvalues)

if __name__ == '__main__':
    # Verbose unittests.
    unittest.main(verbosity=2)
    removedir()