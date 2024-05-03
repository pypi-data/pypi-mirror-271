from collections import namedtuple
import re
import shutil

import dropbox

from django.core.files import File
from django.utils.functional import cached_property
from django.utils.translation import ugettext_lazy as _

from mayan.apps.credentials.class_mixins import BackendMixinCredentials
from mayan.apps.storage.models import SharedUploadedFile
from mayan.apps.storage.utils import NamedTemporaryFile

from .classes import ImportSetupBackend
from .exceptions import ImportSetupException


class ImporterDropbox(BackendMixinCredentials, ImportSetupBackend):
    label = _(message='Dropbox')
    item_identifier = 'id'  # Dropbox file unique identifier.
    item_label = 'name'  # Dropbox file field corresponding to the filename.

    @classmethod
    def get_form_fields(cls):
        fields = super().get_form_fields()

        fields.update(
            {
                'as_team_admin': {
                    'label': _(message='Login as Team administrator'),
                    'class': 'django.forms.BooleanField', 'default': '',
                    'help_text': _(
                        message='Access the API as a Team administrator in order to access '
                        'the entire set of files on a Dropbox Team/Business account. '
                        'If a Team administrator API ID is not specified, it will '
                        'be determined by using the Team API at the cost of an '
                        'extra request per item to process.'
                    ),
                    'required': False
                },
                'team_admin_id': {
                    'label': _(message='Team administrator API ID'),
                    'class': 'django.forms.CharField', 'default': '',
                    'help_text': _(
                        message='An optional Team administrator API to avoid a request '
                        'per item to import.'
                    ),
                    'kwargs': {
                        'max_length': 248
                    }, 'required': False
                },
                'filename_regex': {
                    'label': _(message='Filename regular expression'),
                    'class': 'django.forms.CharField', 'default': '',
                    'help_text': _(
                        message='An optional regular expression used to filter which files '
                        'to import. The regular expression will be matched against '
                        'the filename.'
                    ),
                    'kwargs': {
                        'max_length': 248
                    }, 'required': False
                },
                'folder_regex': {
                    'label': _(message='Folder regular expression'),
                    'class': 'django.forms.CharField', 'default': '',
                    'help_text': _(
                        message='An optional regular expression used to filter which files '
                        'to import. The regular expression will be matched against '
                        'the file folder path.'
                    ),
                    'kwargs': {
                        'max_length': 248
                    }, 'required': False
                },
            }
        )

        return fields

    @classmethod
    def get_form_fieldsets(cls):
        fieldsets = super().get_form_fieldsets()

        fieldsets += (
            (
                _(message='API'), {
                    'fields': ('as_team_admin', 'team_admin_id')
                }
            ), (
                _(message='Content filtering'), {
                    'fields': ('filename_regex', 'folder_regex')
                }
            ),
        )

        return fieldsets

    def get_client_base_kwargs(self):
        credential = self.get_credential()

        try:
            kwargs = {
                'oauth2_access_token': credential['token']
            }
        except KeyError:
            raise ImportSetupException(
                'Incompatible credential class. The credential must provide '
                'an access token.'
            )
        else:
            return kwargs

    @cached_property
    def admin_profile_team_id(self):
        if self.team_admin_id:
            return self.team_admin_id
        else:
            client_kwargs = self.get_client_base_kwargs()
            client_team = dropbox.DropboxTeam(**client_kwargs)
            token_get_authenticated_admin_result = client_team.team_token_get_authenticated_admin()
            return token_get_authenticated_admin_result.admin_profile.team_member_id

    def do_check_valid(self, identifier, data):
        entry = self.get_entry(identifier=identifier, data=data)

        return self.match_filename_factory(entry=entry) and self.match_folder_factory(entry=entry)

    def get_client(self):
        """
        Return an instance of the Dropbox API client.
        """
        kwargs = self.get_client_base_kwargs()

        as_team_admin = self.kwargs['as_team_admin']

        if as_team_admin:
            headers = kwargs.get(
                'headers', {}
            )
            headers.update(
                {
                    'Dropbox-API-Select-User': self.kwargs['admin_profile_team_id']
                }
            )
            kwargs['headers'] = headers

        return dropbox.Dropbox(**kwargs)

    def get_entry(self, identifier, data):
        Entry = namedtuple(
            typename='Entry', field_names=data.keys()
        )
        return Entry(**data)

    def get_item_list(self):
        """
        Crawl the folders and add all the items that are actual files as
        `ImportSetupItem` instances for later processing.
        """
        client = self.get_client()
        response = client.files_list_folder(
            include_non_downloadable_files=False, path='', recursive=True
        )

        while True:
            for entry in response.entries:
                if isinstance(entry, dropbox.files.FileMetadata):
                    # Only add files not directories.

                    if self.match_filename_factory(entry=entry) and self.match_folder_factory(entry=entry):
                        yield {
                            'content_hash': entry.content_hash,
                            'id': entry.id,
                            'name': entry.name,
                            'path_lower': entry.path_lower,
                            'size': entry.size
                        }

            if not response.has_more:
                break
            else:
                response = client.files_list_folder_continue(
                    cursor=response.cursor
                )

    def item_process(self, identifier, data):
        entry = self.get_entry(identifier=identifier, data=data)

        if self.match_filename_factory(entry=entry) and self.match_folder_factory(entry=entry):
            client = self.get_client()

            data, response = client.files_download(
                path=identifier
            )

            response.raise_for_status()

            # Copy the Dropbox file to a temporary location using streaming
            # download.
            # The create a shared upload instance from the temporary file.
            with NamedTemporaryFile() as file_object:
                shutil.copyfileobj(fsrc=response.raw, fdst=file_object)

                file_object.seek(0)

                file = File(file_object)

                return SharedUploadedFile.objects.create(file=file)

    @cached_property
    def match_filename_factory(self):
        """
        Perform a regular expression of and entry's filename.
        Returns True if there is a regular expression match or if there is no
        regular expression set.
        """
        pattern = self.kwargs['filename_regex']

        if pattern:
            regex = re.compile(pattern=pattern)

            def match_function(entry):
                return regex.match(string=entry.name)
        else:
            def match_function(entry):
                return True

        return match_function

    @cached_property
    def match_folder_factory(self):
        """
        Perform a regular expression of and entry's path.
        Returns True if there is a regular expression match or if there is no
        regular expression set.
        """
        pattern = self.kwargs['folder_regex']

        if pattern:
            regex = re.compile(pattern=pattern)

            def match_function(entry):
                return regex.match(string=entry.path_lower)
        else:
            def match_function(entry):
                return True

        return match_function
