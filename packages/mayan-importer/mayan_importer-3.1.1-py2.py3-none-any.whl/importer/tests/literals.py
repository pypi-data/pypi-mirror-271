from pathlib import Path

from django.apps import apps

TEST_IMPORT_SETUP_ITEM_IDENTIFIER = 'test_id_01'
TEST_IMPORT_SETUP_ITEM_IDENTIFIER_EDITED = 'test_id_01_edited'
TEST_IMPORT_SETUP_ITEM_NAME = 'test_item'
TEST_IMPORT_SETUP_ITEM_TIME_BUFFER = 100

TEST_IMPORT_SETUP_LABEL = 'test import setup'
TEST_IMPORT_SETUP_LABEL_EDITED = 'test import setup edited'

TEST_IMPORT_SETUP_PROCESS_SIZE = 1

TEST_IMPORTER_BACKEND_PATH = 'importer.tests.importers.TestImporter'

FILENAME_TEST_FILER_CSV = 'test_importer_setup_item_data.csv'

app_importer = apps.get_app_config(app_label='importer')

PATH_TEST_FILER_CSV = Path(app_importer.path) / 'tests' / 'contrib' / 'test_files' / FILENAME_TEST_FILER_CSV
