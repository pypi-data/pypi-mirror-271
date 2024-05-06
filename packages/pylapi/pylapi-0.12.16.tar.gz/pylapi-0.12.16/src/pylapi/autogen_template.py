# PyLapi API Generator Configuration

# The PyLapi API class name (the common parent of all Resource classes)
# Default: <oas>.info.title in Pascal (upperCamel) case
api_class_name = "MyAPI"

# The output of the generated API
# Overwritable by CLI --output=
# Default: stdout
output_py_name = "./myapi.py"

# The OpenAPI specification (OAS) file in JSON or YAML
# A relative path, if specified, is relative to this config file.
# Default: <this_config_file>.json
oas_file_name = "./myapi_oas.json"

# The authentication type prepended to the "Authentication" header
# Default: Bearer
# api_auth_type = "Bearer"

# The API Server URL
# Default: <oas>.server[0].url
# api_url = "https://api.example.com"

# OpenAPI guide of resource methods
# Default: no guide; overwritable from CLI --guide=
guide_attrs = {
    "summary",
    "description",
    # "parameters",
    # "request_body",
    # "ref",
}
# Note: Including "ref" will dereference all $ref OAS attributes and generates very lengthy guide.

# Naming of resource classes, names, paths, and methods
# Available magic words conversions:
#   snake
#   kebab
#   pascal (upperCamel)
#   camel (lowerCamel)
#   singular
# Required - Modify as needed but DO NOT delete or comment out
naming = {
    # Resource Class Name:
    # class ExampleResource(...):
    # Example: UpperCamel case plus "Resource" for class names
    "class_name": "upperCamel($.path_segments[0]) + 'Resource'",

    # Resource Name used to create a resource object:
    # my_resource = MyAPI.resource("example_resource")
    # Example: Snake case for resource names
    "resource_name": "snake($.path_segments[0])",

    # API path prefix for all methods in the class
    # API full path is {class_path}/{resource_path}
    # Example: resources as in /resources/api_method/...
    # IMPORTANT: Make sure the class_path is common to all methods in the class.
    "class_path": "$.path_segments[0]",

    # API path suffix for the method
    # API full path is {class_path}/{resource_path}
    # Example: api_method as in /resources/api_method/...
    "resource_path": "'/'.join($.path_segments[1:])",

    # Method Name
    # def exampleMethod(self):
    # Example: Lower Camel case for method names
    "method_name": "lowerCamel($.operation_id)",
}

# Optional Code Rewrite script with classes and methods replacing the generated ones
# Default: no code rewrite
# code_rewrite_file_name = "./myapi_rewrite.py"

# Optional resource_class decorator arguments (applied to all resource classes)
# resource_class_args = {"id": "$.id"}

# Optional resource_method decorator arguments (applied to all resource methods)
# resource_method_args = {"send": {"data": "$"}, "give": "$.data"}
