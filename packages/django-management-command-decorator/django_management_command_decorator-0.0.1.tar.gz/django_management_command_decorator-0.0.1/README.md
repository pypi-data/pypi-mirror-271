# Django management command decorator

Small django app to quickly create management commands using a decorating, avoiding writing much boilerplate.


## Installation

* Install this package via pip `pip install django_management_command_decorator`
* Add `management_command_decorator` to your `INSTALLED_APPS` settings
* Create a `commands.py` in your app folder
* Add the `django_management_command` decorator to any function in the `commands.py`


## Usage

Create a `commands.py` in your app, and add the following code:

```python
@django_management_command
def print_command():
    print("Hello World!")

```

You should then be able to call the function from your shell like a management command:

```shell
% python manage.py print_command
Hello World!
```

Function args will be added like management command parameters:

```python
@django_management_command
def greet(name):
    print(f"Hello {name}!")  # noqa: T201
```

```shell
% python manage.py greet Python
Hello Python!
```
