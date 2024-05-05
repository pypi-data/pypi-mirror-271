from mayan.apps.documents.events import (
    event_document_created, event_document_file_created,
    event_document_file_edited, event_document_version_created,
    event_document_version_page_created
)
from mayan.apps.documents.models.document_models import Document
from mayan.apps.documents.tests.base import GenericDocumentViewTestCase

from ..events import (
    event_import_setup_item_finished, event_import_setup_item_created,
    event_import_setup_item_deleted, event_import_setup_item_edited,
    event_import_setup_populate_finished, event_import_setup_populate_started,
    event_import_setup_process_finished, event_import_setup_process_started
)
from ..permissions import (
    permission_import_setup_edit, permission_import_setup_process
)

from .mixins.import_setup_item_mixins import ImportSetupItemViewTestMixin


class ImportSetupItemViewTestCase(
    ImportSetupItemViewTestMixin, GenericDocumentViewTestCase
):
    auto_upload_test_document = False

    def setUp(self):
        super().setUp()
        self._create_test_stored_credential()
        self._create_test_import_setup()

    def test_import_setup_clear_view_no_permission(self):
        self._create_test_import_setup_item()

        import_setup_item_count = self._test_import_setup.items.count()

        self._clear_events()

        response = self._request_test_import_setup_clear_view()
        self.assertEqual(response.status_code, 404)

        self.assertEqual(
            self._test_import_setup.items.count(), import_setup_item_count
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_import_setup_clear_view_with_access(self):
        self._create_test_import_setup_item()

        self.grant_access(
            obj=self._test_import_setup,
            permission=permission_import_setup_process
        )

        import_setup_item_count = self._test_import_setup.items.count()

        self._clear_events()

        response = self._request_test_import_setup_clear_view()
        self.assertEqual(response.status_code, 302)

        self.assertEqual(
            self._test_import_setup.items.count(), import_setup_item_count - 1
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_import_setup_item_delete_view_no_permission(self):
        self._create_test_import_setup_item()

        import_setup_item_count = self._test_import_setup.items.count()

        self._clear_events()

        response = self._request_test_import_setup_item_delete_view()
        self.assertEqual(response.status_code, 404)

        self.assertEqual(
            self._test_import_setup.items.count(), import_setup_item_count
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_import_setup_item_delete_view_with_access(self):
        self._create_test_import_setup_item()

        self.grant_access(
            obj=self._test_import_setup,
            permission=permission_import_setup_edit
        )

        import_setup_item_count = self._test_import_setup.items.count()

        self._clear_events()

        response = self._request_test_import_setup_item_delete_view()
        self.assertEqual(response.status_code, 302)

        self.assertEqual(
            self._test_import_setup.items.count(), import_setup_item_count - 1
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 1)

        self.assertEqual(events[0].action_object, None)
        self.assertEqual(events[0].actor, self._test_import_setup)
        self.assertEqual(events[0].target, self._test_import_setup)
        self.assertEqual(
            events[0].verb, event_import_setup_item_deleted.id
        )

    def test_import_setup_item_edit_view_no_permission(self):
        self._create_test_import_setup_item()

        import_setup_item_label = self._test_import_setup_item.identifier

        self._clear_events()

        response = self._request_test_import_setup_item_edit_view()
        self.assertEqual(response.status_code, 404)

        self._test_import_setup_item.refresh_from_db()
        self.assertEqual(
            self._test_import_setup_item.identifier, import_setup_item_label
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_import_setup_item_edit_view_with_access(self):
        self._create_test_import_setup_item()

        self.grant_access(
            obj=self._test_import_setup,
            permission=permission_import_setup_edit
        )

        import_setup_item_label = self._test_import_setup_item.identifier

        self._clear_events()

        response = self._request_test_import_setup_item_edit_view()
        self.assertEqual(response.status_code, 302)

        self._test_import_setup_item.refresh_from_db()
        self.assertNotEqual(
            self._test_import_setup_item.identifier, import_setup_item_label
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 1)

        self.assertEqual(events[0].action_object, self._test_import_setup)
        self.assertEqual(events[0].actor, self._test_case_user)
        self.assertEqual(events[0].target, self._test_import_setup_item)
        self.assertEqual(
            events[0].verb, event_import_setup_item_edited.id
        )

    def test_import_setup_populate_view_no_permission(self):
        import_setup_item_count = self._test_import_setup.items.count()

        self._clear_events()

        response = self._request_test_import_setup_populate_view()
        self.assertEqual(response.status_code, 404)

        self.assertEqual(
            self._test_import_setup.items.count(), import_setup_item_count
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_import_setup_populate_view_with_access(self):
        self.grant_access(
            obj=self._test_import_setup,
            permission=permission_import_setup_process
        )

        import_setup_item_count = self._test_import_setup.items.count()

        self._clear_events()

        response = self._request_test_import_setup_populate_view()
        self.assertEqual(response.status_code, 302)

        self.assertEqual(
            self._test_import_setup.items.count(), import_setup_item_count + 1
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 4)

        test_import_setup_item = self._test_import_setup.items.first()

        self.assertEqual(events[0].action_object, None)
        self.assertEqual(events[0].actor, self._test_import_setup)
        self.assertEqual(events[0].target, self._test_import_setup)
        self.assertEqual(
            events[0].verb, event_import_setup_populate_started.id
        )

        self.assertEqual(events[1].action_object, self._test_import_setup)
        self.assertEqual(events[1].actor, test_import_setup_item)
        self.assertEqual(events[1].target, test_import_setup_item)
        self.assertEqual(
            events[1].verb, event_import_setup_item_created.id
        )

        self.assertEqual(events[2].action_object, self._test_import_setup)
        self.assertEqual(events[2].actor, test_import_setup_item)
        self.assertEqual(events[2].target, test_import_setup_item)
        self.assertEqual(
            events[2].verb, event_import_setup_item_edited.id
        )

        self.assertEqual(events[3].action_object, None)
        self.assertEqual(events[3].actor, self._test_import_setup)
        self.assertEqual(events[3].target, self._test_import_setup)
        self.assertEqual(
            events[3].verb, event_import_setup_populate_finished.id
        )

    def test_import_setup_process_view_no_permission(self):
        self._create_test_import_setup_item()

        document_count = self._test_document_type.documents.count()

        self._clear_events()

        response = self._request_test_import_setup_process_view()
        self.assertEqual(response.status_code, 404)

        self.assertEqual(
            self._test_document_type.documents.count(), document_count
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_import_setup_process_view_with_access(self):
        self._create_test_import_setup_item()

        self.grant_access(
            obj=self._test_import_setup,
            permission=permission_import_setup_process
        )
        document_count = self._test_document_type.documents.count()

        self._clear_events()

        response = self._request_test_import_setup_process_view()
        self.assertEqual(response.status_code, 302)

        self.assertEqual(
            self._test_document_type.documents.count(), document_count + 1
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 8)

        test_document = Document.objects.last()
        test_document_file = test_document.file_latest
        test_document_version = test_document.versions.last()
        test_document_version_page = test_document_version.pages.first()

        self.assertEqual(events[0].action_object, None)
        self.assertEqual(events[0].actor, self._test_import_setup)
        self.assertEqual(events[0].target, self._test_import_setup)
        self.assertEqual(
            events[0].verb, event_import_setup_process_started.id
        )

        self.assertEqual(events[1].action_object, self._test_document_type)
        self.assertEqual(events[1].actor, test_document)
        self.assertEqual(events[1].target, test_document)
        self.assertEqual(events[1].verb, event_document_created.id)

        self.assertEqual(events[2].action_object, test_document)
        self.assertEqual(events[2].actor, test_document_file)
        self.assertEqual(events[2].target, test_document_file)
        self.assertEqual(events[2].verb, event_document_file_created.id)

        self.assertEqual(events[3].action_object, test_document)
        self.assertEqual(events[3].actor, test_document_file)
        self.assertEqual(events[3].target, test_document_file)
        self.assertEqual(events[3].verb, event_document_file_edited.id)

        self.assertEqual(events[4].action_object, test_document)
        self.assertEqual(events[4].actor, test_document_version)
        self.assertEqual(events[4].target, test_document_version)
        self.assertEqual(events[4].verb, event_document_version_created.id)

        self.assertEqual(events[5].action_object, test_document_version)
        self.assertEqual(events[5].actor, test_document_version_page)
        self.assertEqual(events[5].target, test_document_version_page)
        self.assertEqual(
            events[5].verb, event_document_version_page_created.id
        )

        self.assertEqual(events[6].action_object, self._test_import_setup)
        self.assertEqual(events[6].actor, self._test_import_setup_item)
        self.assertEqual(events[6].target, self._test_import_setup_item)
        self.assertEqual(
            events[6].verb, event_import_setup_item_finished.id
        )

        self.assertEqual(events[7].action_object, None)
        self.assertEqual(events[7].actor, self._test_import_setup)
        self.assertEqual(events[7].target, self._test_import_setup)
        self.assertEqual(
            events[7].verb, event_import_setup_process_finished.id
        )
