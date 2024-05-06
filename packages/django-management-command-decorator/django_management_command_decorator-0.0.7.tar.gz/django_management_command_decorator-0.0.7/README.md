# Django management command decorator

`django_management_command_decorator`is a small Django app to quickly create management commands using a decorator.


## Installation

* Install this package via pip `pip install django_management_command_decorator`
* Add `management_command_decorator` to your `INSTALLED_APPS` settings
* Create a `commands.py` in your app folder
* Add the `django_management_command` decorator to any function you wish to expose as a mangement command in `commands.py`


## Usage

Create a `commands.py` in your app folder, and add the following code:

```python
from management_command_decorator.decorator import django_management_command

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
from management_command_decorator.decorator import django_management_command

@django_management_command
def greet(name):
    print(f"Hello {name}!")
```

```shell
% python manage.py greet Python
Hello Python!
```
