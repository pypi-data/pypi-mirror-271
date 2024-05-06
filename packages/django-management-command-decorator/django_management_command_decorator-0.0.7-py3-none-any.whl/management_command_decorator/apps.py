import importlib
from pathlib import Path

import django
from django.apps import AppConfig
from django.conf import settings

from management_command_decorator.decorator import command_dict


class ManagementCommandDecoratorConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "management_command_decorator"

    def ready(self):
        from django.core.management import get_commands

        old_get_commands = get_commands

        def new_get_commands(*args, **kwargs):
            commands_files = Path(settings.BASE_DIR).glob("**/commands.py")
            for command_file in commands_files:
                *folders, file = command_file.relative_to(settings.BASE_DIR).parts
                module_name = ".".join(folders) + "." + file.replace(".py", "")
                importlib.import_module(module_name)

            commands = old_get_commands(*args, **kwargs)
            for name, cmd in command_dict.items():
                commands[name] = cmd

            return commands

        django.core.management.get_commands = new_get_commands
