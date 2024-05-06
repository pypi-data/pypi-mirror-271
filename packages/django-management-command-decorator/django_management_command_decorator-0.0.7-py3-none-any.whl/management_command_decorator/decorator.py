import functools
import inspect
from argparse import ArgumentParser

from django.core.management import BaseCommand

import wrapt

command_dict = {}


class DecoratedCommand(BaseCommand):
    def __init__(self, func, *args, **kwargs):
        self.func = func
        super().__init__(*args, **kwargs)

    def handle(self, *args, **options):
        parameters = inspect.signature(self.func).parameters
        kwargs = {key: options[key] for key in parameters}
        return self.func(*args, **kwargs)

    def rpartition(self, *args, **kwargs):
        return [self.func.__module__.rpartition(".")[0]]

    def add_arguments(self, parser: ArgumentParser):
        for parameter in inspect.signature(self.func).parameters:
            parser.add_argument(parameter)


def django_management_command(wrapped=None, *, name=None):
    if wrapped is None:
        return functools.partial(django_management_command, name=name)

    @wrapt.decorator
    def wrapper(wrapped, instance, args, kwargs):
        return wrapped(*args, **kwargs)

    command_dict[name if name else wrapped.__name__] = DecoratedCommand(wrapped)
    return wrapper(wrapped)
