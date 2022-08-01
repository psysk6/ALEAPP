"""Integrating teleparser and ALEAPP"""
import sqlite3

import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), "./teleparser/teleparser"))

import tdb
import tblob


def parse_cache_db(files_found, report_folder, seeker, wrap_text):
    print(files_found)
    for file_found in files_found:

        tparse = tblob.tblob()

        file_found = str(file_found)
        if not file_found.endswith("cache4.db"):
            continue  # Skip all other files
        with sqlite3.connect(file_found, uri=True) as db_connection:
            db_connection.text_factory = bytes
            db_connection.row_factory = sqlite3.Row
            db_cursor = db_connection.cursor()
            teledb = tdb.tdb(report_folder, tparse, db_cursor)
            teledb.parse()
        teledb.save_parsed_tables()
        teledb.create_timeline()  # TODO: address crash in this method
