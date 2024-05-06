# PyLapi

Python Lightweight API (PyLapi) is a Python API builder. It takes only a few seconds to automatically generate a Python API from OpenAPI specifications or less than an hour for an experienced Python developer to create a custom Python API.

You can drive PyLapi in an [automatic](./tutorials/2.%20How%20to%20use%20a%20PyLapi%20API.ipynb), [semiautomatic](./tutorials/5.%20PyLapi%20Generator%20Automation.ipynb), or [manual](./tutorials/3.%20A%20ChatGPT%20Conversation%20with%20PyLapi.ipynb) way.
Here is an [overview](./OVERVIEW.md).

## Install PyLapi

Please follow these instructions to install PyLapi and its generator, replacing all variables accordingly.

To install the PyLapi class:
```bash
pip install pylapi
```

To generate a PyLapi supported Python API:

```bash
pylapi-autogen --template > myapi_config.py
# Configure myapi_config.py
pylapi-autogen myapi_config.py
# Output
# MyAPI generated and saved in ./myapi.py
```

## More Information

PyLapi [tutorial](https://github.com/jackyko8/pylapi/blob/main/tutorials) and [user guide](https://github.com/jackyko8/pylapi/blob/main/user_guide) are available at the [PyLapi](https://github.com/jackyko8/pylapi) GitHub repository.
PyLapi API is documented on [Read the Docs](https://pylapi.readthedocs.io/).
