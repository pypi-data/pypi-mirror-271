from django.utils.translation import ugettext_lazy as _

from mayan.apps.task_manager.classes import CeleryQueue, Worker

worker_importer = Worker(
    maximum_memory_per_child=300000, maximum_tasks_per_child=100,
    name='worker_importer'
)

queue_importer = CeleryQueue(
    label=_(message='Importer'), name='importer', worker=worker_importer
)
queue_model_filer = CeleryQueue(
    label=_(message='Model filer'), name='filer', worker=worker_importer
)

queue_importer.add_task_type(
    label=_(message='Process an import setup'),
    dotted_path='importer.tasks.task_import_setup_process'
)
queue_importer.add_task_type(
    label=_(message='Process an import setup item'),
    dotted_path='importer.tasks.task_import_setup_item_process'
)
queue_importer.add_task_type(
    label=_(message='Populate the items of an import setup'),
    dotted_path='importer.tasks.task_import_setup_populate'
)

queue_model_filer.add_task_type(
    label=_(message='Generates CSV files from a model'),
    dotted_path='importer.tasks.task_model_filer_save'
)
queue_model_filer.add_task_type(
    label=_(message='Loads CSV files and created models'),
    dotted_path='importer.tasks.task_model_filer_load'
)
