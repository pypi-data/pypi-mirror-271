import csv
import io
import logging
import shutil

from furl import furl

from django.apps import apps
from django.db import models
from django.urls import reverse
from django.utils.translation import ugettext_lazy as _

from mayan.apps.backends.class_mixins import DynamicFormBackendMixin
from mayan.apps.backends.classes import ModelBaseBackend
from mayan.apps.locales.utils import to_language
from mayan.apps.storage.utils import NamedTemporaryFile

logger = logging.getLogger(name=__name__)

__all__ = ('ImportSetupBackend',)
MESSAGE_MODEL_FILER_SAVE_BODY = _(
    'The model data from object type %(save_file_title)s has been '
    'exported and is available for download using the '
    'link: %(download_url)s or from '
    'the downloads area (%(download_list_url)s).'
)
MESSAGE_MODEL_FILER_SAVE_SUBJECT = _('Model data export.')


class ImportSetupBackend(DynamicFormBackendMixin, ModelBaseBackend):
    _backend_app_label = 'importer'
    _backend_model_name = 'ImportSetup'
    _loader_module_name = 'importers'

    @classmethod
    def callback_document_file(
        cls, document_file, mayan_import_setup_item_id, source_metadata
    ):
        DocumentFileSourceMetadata = apps.get_model(
            app_label='sources', model_name='DocumentFileSourceMetadata'
        )

        coroutine = DocumentFileSourceMetadata.objects.create_bulk()
        next(coroutine)

        for key, value in source_metadata.items():
            coroutine.send(
                {
                    'document_file': document_file, 'key': key, 'value': value
                }
            )

        coroutine.close()

    @classmethod
    def get_form_fieldsets(cls):
        fieldsets = (
            (
                _('General'), {
                    'fields': ('label', 'document_type')
                }
            ), (
                _(message='Processing'), {
                    'fields': ('item_time_buffer', 'process_size', 'state')
                }
            ),
        )

        return fieldsets

    def do_check_valid(self, identifier, data):
        raise NotImplementedError


class NullBackend(ImportSetupBackend):
    label = _(message='Null backend')


class ModelFiler:
    _registry = {}

    @staticmethod
    def get_field_names(model):
        skipped_field_types = (
            models.fields.AutoField, models.fields.related.ForeignKey
        )
        field_names = []

        for field in model._meta.fields:
            if not isinstance(field, skipped_field_types):
                field_names.append(field.name)

        return field_names

    @staticmethod
    def get_full_model_name(model):
        return '{}.{}'.format(model._meta.app_label, model._meta.model_name)

    @classmethod
    def get(cls, full_model_name):
        return cls._registry[full_model_name]

    def __init__(self, model, bulk_size=None):
        self.model = model
        self.bulk_size = bulk_size
        self.__class__._registry[
            ModelFiler.get_full_model_name(model=model)
        ] = self

    def get_model_full_name(self):
        return ModelFiler.get_full_model_name(model=self.model)

    def items_load(self, shared_upload_file, field_defaults=None, user=None):
        if not field_defaults:
            field_defaults = {}

        manager = self.model._meta.default_manager

        if self.bulk_size:
            manager.filter(**field_defaults).delete()
        else:
            for instance in manager.filter(**field_defaults):
                instance.delete()

        with shared_upload_file.open() as file_object_binary:
            with io.TextIOWrapper(file_object_binary) as file_object:
                reader = csv.reader(file_object, delimiter=',')
                header = next(reader)

                reader = csv.DictReader(file_object, fieldnames=header)

                if self.bulk_size:
                    bulk_count = 0
                    bulk_list = []

                    for row in reader:
                        row.update(**field_defaults)
                        model_instance = self.model(**row)
                        bulk_list.append(model_instance)
                        bulk_count += 1

                        if bulk_count > self.bulk_size:
                            manager.bulk_create(bulk_list)
                            bulk_count = 0
                            bulk_list = []

                    manager.bulk_create(bulk_list)
                else:
                    for row in reader:
                        row.update(**field_defaults)
                        manager.create(**row)

    def items_save(
        self, save_file_title, filter_kwargs=None,
        organization_installation_url=None, user=None
    ):
        DownloadFile = apps.get_model(
            app_label='storage', model_name='DownloadFile'
        )
        Message = apps.get_model(
            app_label='messaging', model_name='Message'
        )

        if not filter_kwargs:
            filter_kwargs = {}

        field_names = ModelFiler.get_field_names(model=self.model)

        queryset = self.model._meta.default_manager.filter(**filter_kwargs)

        filename = '{}-export.csv'.format(
            self.get_model_full_name()
        )

        label = _(message='Export of %s to CSV') % save_file_title
        download_file = DownloadFile(
            filename=filename, label=label, user=user
        )
        download_file._event_actor = user
        download_file.save()

        with NamedTemporaryFile(mode='r+') as temporary_file_object:
            writer = csv.DictWriter(
                f=temporary_file_object, fieldnames=field_names
            )

            writer.writeheader()
            for item in queryset.values(*field_names):
                writer.writerow(item)

            temporary_file_object.seek(0)

            with download_file.open(mode='w+') as download_file_object:
                shutil.copyfileobj(
                    fsrc=temporary_file_object, fdst=download_file_object
                )

        if user:
            download_list_url = furl(organization_installation_url).join(
                reverse(
                    viewname='storage:download_file_list'
                )
            ).tostr()

            download_url = furl(organization_installation_url).join(
                reverse(
                    viewname='storage:download_file_download',
                    kwargs={'download_file_id': download_file.pk}
                )
            ).tostr()

            Message.objects.create(
                sender_object=download_file,
                user=user,
                subject=to_language(
                    language=user.locale_profile.language,
                    promise=MESSAGE_MODEL_FILER_SAVE_SUBJECT
                ),
                body=to_language(
                    language=user.locale_profile.language,
                    promise=MESSAGE_MODEL_FILER_SAVE_BODY
                ) % {
                    'download_list_url': download_list_url,
                    'download_url': download_url,
                    'save_file_title': save_file_title
                }
            )
