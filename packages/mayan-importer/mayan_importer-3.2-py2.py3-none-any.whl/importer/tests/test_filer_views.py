from mayan.apps.documents.tests.base import GenericDocumentViewTestCase

from ..events import event_import_setup_item_created
from ..permissions import permission_model_filer_load

from .mixins.filer_mixins import FilerTestViewMixin


class FilerViewTestCase(FilerTestViewMixin, GenericDocumentViewTestCase):
    def test_import_setup_load_view_with_access(self):
        self.grant_access(
            obj=self._test_import_setup,
            permission=permission_model_filer_load
        )

        import_setup_item_count = self._test_import_setup.items.count()

        self._clear_events()

        response = self._request_test_import_setup_load_view()
        self.assertEqual(response.status_code, 302)

        self.assertEqual(
            self._test_import_setup.items.count(), import_setup_item_count + 1
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 1)

        test_import_setup_item = self._test_import_setup.items.first()

        self.assertEqual(events[0].action_object, self._test_import_setup)
        self.assertEqual(events[0].actor, test_import_setup_item)
        self.assertEqual(events[0].target, test_import_setup_item)
        self.assertEqual(
            events[0].verb, event_import_setup_item_created.id
        )
