from collections import namedtuple
import shutil

from django.core.files import File
from django.utils.translation import ugettext_lazy as _

from mayan.apps.documents.tests.literals import TEST_FILE_SMALL_PATH
from mayan.apps.storage.models import SharedUploadedFile
from mayan.apps.storage.utils import NamedTemporaryFile

from ..classes import ImportSetupBackend

from .literals import (
    TEST_IMPORT_SETUP_ITEM_IDENTIFIER, TEST_IMPORT_SETUP_ITEM_NAME
)

TestImporterItem = namedtuple(
    typename='TestItem', field_names=('id', 'name',)
)


class TestImporter(ImportSetupBackend):
    label = _('Test importer')
    item_identifier = 'id'
    item_label = 'name'

    @staticmethod
    def get_test_item():
        return TestImporterItem(
            id=TEST_IMPORT_SETUP_ITEM_IDENTIFIER,
            name=TEST_IMPORT_SETUP_ITEM_NAME
        )

    @staticmethod
    def get_item_list():
        return [
            TestImporter.get_test_item()
        ]

    def do_check_valid(self, identifier, data):
        return True

    def item_process(self, identifier, data):
        # Copy the Dropbox file to a temporary location using streaming
        # download.
        # The create a shared upload instance from the temporary file.
        with open(TEST_FILE_SMALL_PATH, mode='rb') as document_file_object:
            with NamedTemporaryFile() as file_object:
                shutil.copyfileobj(
                    fsrc=document_file_object, fdst=file_object
                )

                file_object.seek(0)

                return SharedUploadedFile.objects.create(
                    file=File(file_object),
                )
