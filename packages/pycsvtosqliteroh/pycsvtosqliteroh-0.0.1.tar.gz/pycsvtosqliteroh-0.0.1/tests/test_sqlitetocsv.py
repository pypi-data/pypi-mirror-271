"""Testing the module with the python internal unittest module."""

# Import necessary modules.
import unittest
import os
import sqlite3
# User defined modules.
from src.pycsvtosqliteroh import SqliteToCsv
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
            file_list.append(file)
    return file_list

# Get filenames.
def get_filenames(dir: str):
    filelist = []
    for file in os.listdir(dir):
        filelist.append(Path(file))
    return filelist

def remove_extension(file: str):
    name_without_extension = os.path.splitext(file)[0]
    return name_without_extension

# Testing main functions.
class TestPycsvtosqliteroh_sqlitetocsv(unittest.TestCase):
    
    def setUp(self):
        self.path = "./tests/testfiles"
        self.files = get_testfiles(self.path)
        self.database = "./Test.sqlite"
        self.newfilepath = "./exportedfiles"

    def test_convert_table_to_csv(self):
        with _Database(self.database) as db:
            for file in self.files:
                sqliteobj = SqliteToCsv(self.database, os.path.join(self.newfilepath, file), remove_extension(file))
                sqliteobj.convert_table_to_csv()

    def test_if_files_created(self):
        oldfiles = get_filenames(self.path)
        for file in oldfiles:
            self.assertTrue(os.path.exists(os.path.join(self.newfilepath, file)))

if __name__ == '__main__':
    # Verbose unittests.
    unittest.main(verbosity=2)
    removedir()