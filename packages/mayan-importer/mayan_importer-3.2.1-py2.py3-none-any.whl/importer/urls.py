from django.conf.urls import url

from .api_views import (
    APIImportSetupClearView, APIImportSetupDetailView,
    APIImportSetupListView, APIImportSetupPopulateView,
    APIImportSetupProcessView, APIImportSetupItemDetailView,
    APIImportSetupItemListView
)
from .views.import_setup_filer_views import (
    ImportSetupFilerLoadView, ImportSetupFilerSaveConfirmView
)
from .views.import_setup_item_views import (
    ImportSetupItemDeleteView, ImportSetupItemDocumentListView,
    ImportSetupItemEditView, ImportSetupItemListView,
    ImportSetupItemProcessView
)
from .views.import_setup_views import (
    ImportSetupBackendSelectionView, ImportSetupClearView,
    ImportSetupCreateView, ImportSetupDeleteView, ImportSetupEditView,
    ImportSetupListView, ImportSetupPopulateView, ImportSetupProcessView
)


urlpatterns_import_setup = [
    url(
        regex=r'^import_setups/$', name='import_setup_list',
        view=ImportSetupListView.as_view()
    ),
    url(
        regex=r'^import_setups/backend/selection/$',
        name='import_setup_backend_selection',
        view=ImportSetupBackendSelectionView.as_view()
    ),
    url(
        regex=r'^import_setups/(?P<backend_path>[a-zA-Z0-9_.]+)/create/$',
        name='import_setup_create',
        view=ImportSetupCreateView.as_view()
    ),
    url(
        regex=r'^import_setups/(?P<import_setup_id>\d+)/delete/$',
        name='import_setup_delete', view=ImportSetupDeleteView.as_view()
    ),
    url(
        regex=r'^import_setups/(?P<import_setup_id>\d+)/edit/$',
        name='import_setup_edit', view=ImportSetupEditView.as_view()
    )
]

urlpatterns_import_setup_filer = [
    url(
        regex=r'^import_setups/(?P<import_setup_id>\d+)/load/$',
        name='import_setup_load', view=ImportSetupFilerLoadView.as_view()
    ),
    url(
        regex=r'^import_setups/(?P<import_setup_id>\d+)/save/$',
        name='import_setup_save',
        view=ImportSetupFilerSaveConfirmView.as_view()
    )
]


urlpatterns_import_setup_items = [
    url(
        regex=r'^import_setups/(?P<import_setup_id>\d+)/clear/$',
        name='import_setup_clear',
        view=ImportSetupClearView.as_view()
    ),
    url(
        regex=r'^import_setups/multiple/clear/$',
        name='import_setup_multiple_clear',
        view=ImportSetupClearView.as_view()
    ),
    url(
        regex=r'^import_setups/(?P<import_setup_id>\d+)/populate/$',
        name='import_setup_populate_single',
        view=ImportSetupPopulateView.as_view()
    ),
    url(
        regex=r'^import_setups/multiple/populate/$',
        name='import_setup_populate_multiple',
        view=ImportSetupPopulateView.as_view()
    ),
    url(
        regex=r'^import_setups/(?P<import_setup_id>\d+)/process/$',
        name='import_setup_process_single',
        view=ImportSetupProcessView.as_view()
    ),
    url(
        regex=r'^import_setups/multiple/process/$',
        name='import_setup_process_multiple',
        view=ImportSetupProcessView.as_view()
    ),
    url(
        regex=r'^import_setups/(?P<import_setup_id>\d+)/items/$',
        name='import_setup_items_list',
        view=ImportSetupItemListView.as_view()
    ),
    url(
        regex=r'^import_setups/items/(?P<import_setup_item_id>\d+)/delete/$',
        name='import_setup_item_delete_single',
        view=ImportSetupItemDeleteView.as_view()
    ),
    url(
        regex=r'^import_setups/items/multiple/delete/$',
        name='import_setup_item_delete_multiple',
        view=ImportSetupItemDeleteView.as_view()
    ),
    url(
        regex=r'^import_setups/items/(?P<import_setup_item_id>\d+)/documents/$',
        name='import_setup_item_document_list',
        view=ImportSetupItemDocumentListView.as_view()
    ),
    url(
        regex=r'^import_setups/items/(?P<import_setup_item_id>\d+)/delete/$',
        name='import_setup_item_delete',
        view=ImportSetupItemDeleteView.as_view()
    ),
    url(
        regex=r'^import_setups/items/(?P<import_setup_item_id>\d+)/edit/$',
        name='import_setup_item_edit',
        view=ImportSetupItemEditView.as_view()
    ),
    url(
        regex=r'^import_setups/items/multiple/process/$',
        name='import_setup_item_process_multiple',
        view=ImportSetupItemProcessView.as_view()
    ),
    url(
        regex=r'^import_setups/items/(?P<import_setup_item_id>\d+)/process/$',
        name='import_setup_item_process_single',
        view=ImportSetupItemProcessView.as_view()
    ),
]

urlpatterns = []
urlpatterns.extend(urlpatterns_import_setup)
urlpatterns.extend(urlpatterns_import_setup_filer)
urlpatterns.extend(urlpatterns_import_setup_items)

api_urls = [
    url(
        regex=r'^import_setups/$', name='importsetup-list',
        view=APIImportSetupListView.as_view()
    ),
    url(
        regex=r'^import_setups/(?P<import_setup_id>[0-9]+)/$',
        name='importsetup-detail', view=APIImportSetupDetailView.as_view()
    ),
    url(
        regex=r'^import_setups/(?P<import_setup_id>[0-9]+)/clear/$',
        name='importsetup-clear', view=APIImportSetupClearView.as_view()
    ),
    url(
        regex=r'^import_setups/(?P<import_setup_id>[0-9]+)/populate/$',
        name='importsetup-populate', view=APIImportSetupPopulateView.as_view()
    ),
    url(
        regex=r'^import_setups/(?P<import_setup_id>[0-9]+)/process/$',
        name='importsetup-process', view=APIImportSetupProcessView.as_view()
    ),
    url(
        regex=r'^import_setups/(?P<import_setup_id>[0-9]+)/items/$',
        name='importsetupitem-list', view=APIImportSetupItemListView.as_view()
    ),
    url(
        regex=r'^import_setups/(?P<import_setup_id>[0-9]+)/items/(?P<import_setup_item_id>[0-9]+)/$',
        name='importsetupitem-detail',
        view=APIImportSetupItemDetailView.as_view()
    )
]
