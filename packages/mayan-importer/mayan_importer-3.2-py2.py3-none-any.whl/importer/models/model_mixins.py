from django.db import models
import django.db.models.options as options
from django.utils.module_loading import import_string
from django.utils.translation import ugettext_lazy as _


class ModelMixinState(models.Model):
    state = models.PositiveIntegerField(
        blank=True, help_text=_(
            message='The current condition or configuration of the object. '
            'This is managed automatically by the system. Only change '
            'the state if the object\'s task is stale or orphaned.'
        ), verbose_name=_(message='State')
    )

    class Meta:
        abstract = True

    @staticmethod
    def do_options_monkeypatch():
        # Ugly hack but Django does not offer any other method.

        is_patched = getattr(ModelMixinState, 'is_patched', False)

        if not is_patched:
            options.DEFAULT_NAMES = options.DEFAULT_NAMES + (
                'state_choices', 'state_default'
            )
            setattr(ModelMixinState, 'is_patched', True)

    def do_state_set(self, state):
        self.state = state
        self._event_ignore = True
        self.save(
            update_fields=('state',)
        )

    def get_state_label(self):
        choices = dict(self._meta.state_choices)
        unknown_state_label = _(
            message='Unknown state `{}`'.format(self.state)
        )
        return choices.get(self.state, unknown_state_label)

    get_state_label.help_text = _(
        message='The last recorded state of the object. The field will '
        'be sorted by the numeric value of the state and not the actual '
        'text.'
    )
    get_state_label.short_description = _(message='State')

    def save(self, *args, **kwargs):
        if not self.state:
            state_default = self._meta.state_default
            self.state = state_default

        super().save(*args, **kwargs)


class ModelMixinTaskMethod:
    @staticmethod
    def do_options_monkeypatch():
        # Ugly hack but Django does not offer any other method.

        is_patched = getattr(ModelMixinTaskMethod, 'is_patched', False)

        if not is_patched:
            options.DEFAULT_NAMES = options.DEFAULT_NAMES + (
                'task_name_list',
            )
            setattr(ModelMixinTaskMethod, 'is_patched', True)

    def __getattr__(self, name):
        prefix = 'queue_'

        task_name = name[len(prefix):]

        if task_name in self._meta.task_name_list:
            app_path = self._meta.app_config.name
            dotted_path = '{}.tasks.{}'.format(app_path, task_name)
            task = import_string(dotted_path=dotted_path)

            full_method_name_pre = '{}_pre'.format(name)
            full_method_name_post = '{}_post'.format(name)

            def wrapper(**kwargs):
                function_pre = getattr(self, full_method_name_pre, None)
                if function_pre:
                    function_pre()

                task.apply_async(**kwargs)

                function_post = getattr(self, full_method_name_post, None)
                if function_post:
                    function_post()

            return wrapper

        return self.__getattribute__(name)


ModelMixinState.do_options_monkeypatch()
ModelMixinTaskMethod.do_options_monkeypatch()
