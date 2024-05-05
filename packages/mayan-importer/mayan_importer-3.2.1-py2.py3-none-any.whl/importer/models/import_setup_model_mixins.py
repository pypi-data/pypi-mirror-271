from datetime import datetime, timedelta

from django.apps import apps
from django.conf import settings
from django.contrib.humanize.templatetags.humanize import intcomma
from django.utils.translation import gettext_lazy as _

from ..events import (
    event_import_setup_populate_finished, event_import_setup_populate_started,
    event_import_setup_process_finished, event_import_setup_process_started
)
from ..literals import (
    IMPORT_SETUP_ITEM_STATE_PROCESSED, IMPORT_SETUP_STATE_ERROR,
    IMPORT_SETUP_STATE_NONE, IMPORT_SETUP_STATE_POPULATING,
    IMPORT_SETUP_STATE_POPULATED, IMPORT_SETUP_STATE_PROCESSING,
    IMPORT_SETUP_STATE_PROCESSED
)


class ImportSetupBusinessLogicMixin:
    @classmethod
    def get_process_allowed_state_list(self):
        return (
            IMPORT_SETUP_STATE_ERROR, IMPORT_SETUP_STATE_NONE,
            IMPORT_SETUP_STATE_POPULATED, IMPORT_SETUP_STATE_PROCESSED
        )

    def do_clear(self):
        self.items.all().delete()

    def do_populate(self, force=False, user=None):
        if force or self.get_process_allowed():
            event_import_setup_populate_started.commit(
                actor=user, target=self
            )

            self.do_state_set(state=IMPORT_SETUP_STATE_POPULATING)

            try:
                backend_instance = self.get_backend_instance()

                for item in backend_instance.get_item_list():

                    identifer_field = backend_instance.item_identifier
                    try:
                        # Try as an attribute.
                        identifier = getattr(item, identifer_field)
                    except (AttributeError, TypeError):
                        # Try as dictionary.
                        identifier = item[identifer_field]

                    setup_item, created = self.items.get_or_create(
                        identifier=identifier
                    )
                    if created:
                        setup_item.do_data_dump(obj=item)
                        setup_item.save()
            except Exception as exception:
                self.do_state_set(state=IMPORT_SETUP_STATE_ERROR)

                self.error_log.create(
                    text='{}; {}'.format(
                        exception.__class__.__name__, exception
                    )
                )
                if settings.DEBUG:
                    raise
            else:
                self.do_state_set(state=IMPORT_SETUP_STATE_POPULATED)

                event_import_setup_populate_finished.commit(
                    actor=user, target=self
                )

                queryset_logs = self.error_log.all()
                queryset_logs.delete()

    def do_process(self, force=False, user=None):
        """
        Iterate of the `ImportSetupItem` instances downloading and creating
        documents from them.
        """
        if force or self.get_process_allowed():
            self.do_state_set(state=IMPORT_SETUP_STATE_PROCESSING)

            event_import_setup_process_started.commit(
                actor=user, target=self
            )

            try:
                count = 0
                eta = datetime.utcnow()
                # Only schedule items that have not succeeded in being
                # imported.
                ImportSetupItem = apps.get_model(
                    app_label='importer', model_name='ImportSetupItem'
                )
                queryset = self.items.filter(
                    state__in=ImportSetupItem.get_process_allowed_state_list()
                )
                iterator = queryset.iterator()

                while True:
                    item = next(iterator)
                    if item.do_check_valid():
                        count = count + 1
                        eta += timedelta(milliseconds=self.item_time_buffer)
                        item.queue_task_import_setup_item_process(
                            eta=eta, kwargs={'import_setup_item_id': item.pk}
                        )

                        if count >= self.process_size:
                            break

            except StopIteration:
                """
                Expected exception when iterator is exhausted before the
                process size is reached.
                """
            except Exception as exception:
                self.do_state_set(state=IMPORT_SETUP_STATE_ERROR)

                self.error_log.create(
                    text=str(exception)
                )

                if settings.DEBUG:
                    raise

                # Exit the method to avoid committing the ended event.
                return

            # This line is reached on `StopIteration` or from the break in the
            # loop.
            self.do_state_set(state=IMPORT_SETUP_STATE_PROCESSED)

            queryset = self.error_log.all()
            queryset.delete()

            event_import_setup_process_finished.commit(actor=user, target=self)

    def get_item_all_count(self):
        queryset = self.items.all()
        return queryset.count()

    get_item_all_count.short_description = _(message='Items')

    def get_item_processed_count(self):
        queryset = self.items.filter(state=IMPORT_SETUP_ITEM_STATE_PROCESSED)
        return queryset.count()

    get_item_processed_count.short_description = _(message='Items complete')

    def get_item_processed_percent(self):
        items_complete = self.get_item_processed_count()
        items_all = self.get_item_all_count()

        if items_all == 0:
            percent = 0
        else:
            percent = items_complete / items_all * 100.0

        return '{} of {} ({:.0f}%)'.format(
            intcomma(value=items_complete), intcomma(value=items_all),
            percent
        )

    get_item_processed_percent.short_description = _(message='Progress')

    def get_process_allowed(self):
        return self.state in self.get_process_allowed_state_list()

    get_process_allowed.short_description = _(message='Can be processed?')
