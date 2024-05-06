from django.core.management import call_command

from management_command_decorator.commands import print_command, print_command_2


def test_call_command():
    call_command("print_command")


def test_call_other_command():
    call_command("other_command")


def test_print_command_as_func():
    # test we don't crash
    print_command()
    print_command_2()


def test_command_with_args():
    call_command("print_command_with_args", "name")
