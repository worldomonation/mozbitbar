# Mozbitbar

Mozbitbar is a wrapper around Bitbar's [Testdroid](https://github.com/bitbar/testdroid-api-client-python) API client for Python2.

Mozbitbar implements a subset of tasks that Testdroid supports, but aims to make the process of starting Bitbar tasks easier and better defined through the use of _recipes_.


## Invocation

Since Mozbitbar currently does not support installation via a package manager, users are recommended to use the following syntax, in the root directory of Mozbitbar:

```
$ export PYTHONPATH=.
$ python mozbitbar/main.py --recipe <full_path_to_recipe>
```

## Usage

Define a recipe under `mozbitbar/recipes` subdirectory.

Recipes must be in valid YAML format. If unsure, ensure the recipe can be parsed by PyYAML.

An example of the expected format of the recipe can be seen below:

````
- action: create_project
  arguments:
    name: hello_world
    type: DEFAULT
````

There are specific rules that must be followed in order to create a valid Mozbitbar recipe, which will be covered below.

## Defining a recipe

### action

`action` is a top level command in the recipe. Using action, the recipe writer is able to instruct Mozbitbar to call specific actions implemented in the module.

Therefore the `action` command must map to a valid action in the BitbarProject object.

### arguments

`arguments` is the subcommand in the recipe. It must be preceded by an `action` command and is used to pass arguments into the Python method that implements the action.

For example. in the above example, the `create_project` action requires two arguments to be passed: `name`, which is the project name, and `type` which is the project type.

### arguments themselves

Following the `arguments` subcommand is the list of arguments to be passed into the method. These are key:value pairs and the key must correspond to the parameter name.

## Other Notes

It is recommended to use a virtual environment with Mozbitbar.
