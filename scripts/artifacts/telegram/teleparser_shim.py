"""Integrating teleparser and ALEAPP"""
import sqlite3

import os
import sys
from scripts.artifact_report import ArtifactHtmlReport

sys.path.append(os.path.join(os.path.dirname(__file__), "./teleparser/teleparser"))

import tdb
import tblob


FIELDS = [
    "timestamp",
    "source",
    "id",
    "type",
    "from",
    "from_id",
    "to",
    "to_id",
    "dialog",
    "dialog_type",
    "content",
    "media",
    "extra",
]


def format_telegram_artefacts(f_tdb: tdb.tdb) -> list:
    """Attempting to parse telelgram tdb artefact without modifying teleparser

    Args:
        tdb (tdb.tdb): parsed database

    Returns:
        list: Returns data in format for ALEAPP
    """
    table_rows = list()
    for row in f_tdb.get_chats_timeline():
        table_rows.append(row.row_to_tuple())
    for row in f_tdb.get_dialogues_timeline():
        table_rows.append(row.row_to_tuple())
    for row in f_tdb.get_enc_chats_timeline():
        table_rows.append(row.row_to_tuple())
    for row in f_tdb.get_users_timeline():
        table_rows.append(row.row_to_tuple())
    for row in f_tdb.get_messages_timeline():
        table_rows.append(row.row_to_tuple())
    return table_rows


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

        data_rows = format_telegram_artefacts(teledb)
        if len(data_rows) > 0:
            report = ArtifactHtmlReport("Telegram Artefacts")
            report.start_artifact_report(report_folder, "Telegram Message")
            report.write_artifact_data_table(
                FIELDS, data_rows, file_found, html_escape=False
            )
