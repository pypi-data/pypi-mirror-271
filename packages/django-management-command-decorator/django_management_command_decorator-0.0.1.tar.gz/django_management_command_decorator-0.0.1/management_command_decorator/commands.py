from management_command_decorator.decorator import django_management_command


@django_management_command
def print_command():
    print("Hello World!")  # noqa: T201


@django_management_command(name="other_command")
def print_command_2():
    print("Hello other World!")  # noqa: T201


@django_management_command
def print_command_with_args(name):
    print(f"Hello {name}")  # noqa: T201
