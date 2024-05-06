# PyLapi API Generator
#
# This script generates a PyLapi API from a configuration file.
#
# Steps:
# 1. Create a configuration file from the configuration template.
# 2. Customise the configuration file by following the instructions in the comment.
# 3. Run this script with the configuration file as the first argument.
#   - The OpenAPI specification JSON file is specified
#     - as the second argument, or if not specified
#     - in the configuration file `oas` variable, or if not specified
#     - as the configuration file name, with .py replaced by .json
#   - The OpenAPI JSON file path is either absolute or relative to the current directory.

import json
import yaml
import re
import sys
import os
from enum import IntEnum
from getopt import getopt, GetoptError
from magico import MagicO


# Defaults
debug = False
oas_spec = {}
output_py = None
output_py_name = None
guide_attrs = None

all_guide_attrs = {
    "summary",
    "description",
    "parameters",
    "request_body",
}

control_guide_attrs = {
    "ref",
    "all",
}

config_file = ""

main_basename = os.path.basename(sys.argv[0]).rstrip('.py')

def usage(exit_code=0):
    print(f"""Usage: {main_basename} [options ...] <config.py> [<openapi.json/yaml]
\t-h --help           Print this help message
\t-o --output=<file>  Output the API SDK to <file> instead of stdout
\t-g --guide=<list>   Include some OpenAI attributes as comments; the list is comma-deliminted list with no spaces.
\t                    Valid attributes include: summary,description,parameters,request_body,all,ref
\t                    `all` means to include all items on the list
\t                    `ref` means to dereference $ref cells in OpenAI attributes
\t-t --template       Print the autogen configuration template to stdout
\t-d --debug          Print all the methods to be generated then stop""", file=sys.stderr)
    exit(exit_code)


valid_guide_attrs = all_guide_attrs.union(control_guide_attrs)

code_rewrite_lines = []
snippets = MagicO({})

# For naming conversion, use MagicWords(name).<conversion>, where <conversion> can be
# snake, kebab, pascal (upperCamel), camel (lowerCamel), or singular
# e.g., MagicWords("ThisIs a good_test for magic-words_conversion.").snake
#       Output: this_is_a_good_test_for_magic_words_conversion
def snake(phrase): return MagicWords(phrase).snake
def kebab(phrase): return MagicWords(phrase).kebab
def upperCamel(phrase): return MagicWords(phrase).upperCamel
def lowerCamel(phrase): return MagicWords(phrase).lowerCamel
def pascal(phrase): return MagicWords(phrase).pascal
def camel(phrase): return MagicWords(phrase).camel
def singular(phrase): return MagicWords(phrase).singular


class Method():
    def __init__(self, config, method):
        self.config = config
        self.method = method
        self.path_segments = self.method["path"].strip("/").split("/")

    def __repr__(self):
        return str(self.method)

    @property
    def api_path(self):
        _api_path = "/" + self.class_path if self.class_path else ""
        _api_path += "/" + self.resource_path if self.resource_path else ""
        return _api_path

    ########################################
    #
    # Derived attributes - customisables
    #   These attributes are derived from the original OpenAPI JSON
    #   attributes as described in the next section.
    #

    @property
    def class_name(self):
        # return MagicWords(MagicWords(self.path_segments[0]).singular).upperCamel + "Resource"
        return eval(self.config.naming["class_name"].replace("$", "self"))

    # Resource Name used to create a resource object:
    # my_resource = MyAPI.resource("example_resource")
    # Example: Singular snake case for resource names
    @property
    def resource_name(self):
        # return MagicWords(MagicWords(self.path_segments[0]).singular).snake
        return eval(self.config.naming["resource_name"].replace("$", "self"))

    # API path prefix for all methods in the class
    # API full path is {class_path}/{resource_path}
    # Example: resources in /resources/api_method/...
    # IMPORTANT: Make sure the class_path is common to all methods in the class.
    @property
    def class_path(self):
        # return self._path_segments[0]
        # return ""
        return eval(self.config.naming["class_path"].replace("$", "self"))

    # API path suffix for the method
    # API full path is {class_path}/{resource_path}
    # Example: api_method in /resources/api_method/...
    @property
    def resource_path(self):
        # return "/".join(self._path_segments[1:])
        # return "/".join(self.path_segments)
        return eval(self.config.naming["resource_path"].replace("$", "self"))

    # Method Name
    # def exampleMethod(self):
    # Example: Lower Camel case for method names
    @property
    def method_name(self):
        # return MagicWords(self.operation_id).lowerCamel
        return eval(self.config.naming["method_name"].replace("$", "self"))


    ########################################
    #
    # Initialised attributes - not to be customised
    #   These attributes are captured from the
    #   OpenAPI JSON file, and returned without
    #   conversion (except http_method to uppercase).
    #
    @property
    def path(self):
        return self.method["path"]

    @property
    def http_method(self):
        return self.method["http_method"].upper()

    @property
    def operation_id(self):
        return self.method["operation_id"]

    # The followings are used for documentation in the generated file.
    # Comment out, or return blank, None, or False to suppress.
    @property
    def summary(self):
        return self.method["summary"]

    @property
    def description(self):
        return self.method["description"]

    @property
    def parameters(self):
        return self.method["parameters"]

    @property
    def request_body(self):
        return self.method["request_body"]


def dict_checked(dict_data, attr, default=""):
    return dict_data[attr] if attr in dict_data else default


def print_error(err=""):
    print(err, file=sys.stderr)


def print_line(line=""):
    if line != None:
        print(line.rstrip(), file=output_py)


def get_oas_spec(oas_file_name):
    global config_file
    _oas_spec = {}
    _oas_type = re.sub(r".+\.(json|yaml)$", "\\1", oas_file_name)

    try:
        if _oas_type == "json":
            _oas_spec = json.load(open(oas_file_name, "r"))
        elif _oas_type == "yaml":
            _oas_spec = yaml.safe_load(open(oas_file_name, "r"))
        else:
            raise Exception(f"Unknown OpenAI specification file type: {oas_file_name}")
    except:
        raise Exception(f"Cannot open OpenAI specification file: {oas_file_name}\nSuggest checking configuration file: {config_file}")

    for _ in ("openapi", "paths"):
        if _ not in _oas_spec:
            raise Exception(f'OpenAI Error: No "{_}" found in {oas_file_name}')

    return _oas_spec


def set_config(config, _oas_spec):
    # Get all config settings defined
    # Missing settings will be taken from _oas_spec

    # config.api_class_name fallback on oas.info.title
    try:
        _ = config.api_class_name  # A trivial check
    except:
        try:
            api_class_name = upperCamel(_oas_spec["info"]["title"])
        except:
            raise Exception(f"API class name cannot be determined: Neither in config and nor in OpenAI specification")
        else:
            config.api_class_name = api_class_name

    # config.api_url fallback on oas.servers[0].url
    try:
        api_url = config.api_url  # A trivial check
    except:
        try:
            api_url = _oas_spec["servers"][0]["url"]
        except:
            raise Exception(f"API URL cannot be determined: Neither in config and nor in OpenAI specification")
        else:
            config.api_url = api_url


class RewriteExpect(IntEnum):
    CLASS_API = 0
    CLASS_DECO = 1
    CLASS_DEF = 2
    METHOD_DECO = 3
    METHOD_DEF = 4

def get_code_rewrite(config, code_rewrite_file_name):
    global snippets
    global code_rewrite_lines

    if not code_rewrite_file_name:
        return

    code_rewrite_lines = [_.rstrip() for _ in open(code_rewrite_file_name, "r").readlines()]
    # print(len(code_rewrite_lines))

    # {"resource": (slice_from, slice_to)}
    # where "resource" being one of these:
    # "" - opening lines
    # "{method.class_name}" - a class
    # "{method.class_name}.{method.method_name}" - a method
    # If "resource" is "", expect a class, else except a class or a method

    this_snippet = "@"  # Opening
    this_class = ""  # Current class the line is in
    this_slice = [0]
    snippets[this_snippet] = this_slice
    expect = (RewriteExpect.CLASS_API, RewriteExpect.CLASS_DECO)
    line = -1  # In case the file is empty
    for line in range(len(code_rewrite_lines)):
        # print(f"line {line}")
        code_rewrite_line = code_rewrite_lines[line]
        # Strategy: Most frequent cases checked first
        if RewriteExpect.METHOD_DECO in expect:
            if re.findall(rf"^\s*@{config.api_class_name}\.resource_method", code_rewrite_line):
                # print(f"MDC {line+1}: {code_rewrite_line}")
                this_slice.append(line)  # Complete `this` first
                snippets[this_snippet] = this_slice
                this_slice = [line]  # Mark the new
                expect = (RewriteExpect.METHOD_DEF,)
                # print(f"expect {expect}")
                continue
        if RewriteExpect.METHOD_DEF in expect:
            method_name = re.findall(rf"^\s*def\s+([^(]+)\(", code_rewrite_line)
            if len(method_name):
                # print(f"MDF {line+1}: {code_rewrite_line}")
                method_name = method_name[0]
                this_snippet = f"{this_class}.{method_name}"
                expect = (RewriteExpect.METHOD_DECO, RewriteExpect.CLASS_DECO)
                # print(f"expect {expect}")
                continue
        if RewriteExpect.CLASS_DECO in expect:
            if re.findall(rf"^\s*@{config.api_class_name}\.resource_class", code_rewrite_line):
                # print(f"CDC {line+1}: {code_rewrite_line}")
                this_slice.append(line)  # Complete `this` first
                snippets[this_snippet] = this_slice
                this_slice = [line]  # Mark the new
                expect = (RewriteExpect.CLASS_DEF,)
                # print(f"expect {expect}")
                continue
        if RewriteExpect.CLASS_DEF in expect:
            class_name = re.findall(rf"^\s*class\s+([^(]+)\(", code_rewrite_line)
            if len(class_name):
                # print(f"CDF {line+1}: {code_rewrite_line}")
                this_class = class_name[0]
                this_snippet = f"{this_class}.@"
                expect = (RewriteExpect.METHOD_DECO, RewriteExpect.CLASS_DECO)
                # print(f"expect {expect}")
                continue
        if RewriteExpect.CLASS_API in expect:
            if re.findall(rf"^\s*class {config.api_class_name}\(", code_rewrite_line):
                # print(f"API {line+1}: {code_rewrite_line}")
                this_slice.append(line)  # Complete `this` first
                snippets[this_snippet] = this_slice
                this_slice = [line]  # Mark the new
                this_snippet = f"{config.api_class_name}.@"
                expect = (RewriteExpect.CLASS_DECO,)
                # print(f"expect {expect}")
                continue

    # Complete the last snippet
    this_slice.append(line+1)
    snippets[this_snippet] = this_slice


def rewrite_me(snippet_name, intro_line=None):
    _intro_line = None
    _code_lines = None
    _co = ""
    if snippet_name in snippets:
        _code_lines = "\n".join(code_rewrite_lines[slice(*snippets[snippet_name])])
        if intro_line and _code_lines.rstrip():
            leading_spaces = re.findall(r"^(\s*)\S", _code_lines)
            line_indent = ""
            if len(leading_spaces):
                line_indent = leading_spaces[0]
            # Always a space line before
            _intro_line = f"\n{line_indent}# {intro_line}"
        _co = "# "
        del snippets[snippet_name]
    return _intro_line, _code_lines, _co


def get_methods(config, oas_paths):
    methods = []
    for oas_path in oas_paths:  # Loop through each API path in OAS
        oas_http_methods = oas_paths[oas_path]  # A list of HTTP methods, e.g., "get"
        if "parameters" in oas_http_methods:  # "parameters" is NOT an HTTP method
            del oas_http_methods["parameters"]
        for oas_http_method in oas_http_methods:  # Loop through each HTTP method the path supports
            oas_method = oas_http_methods[oas_http_method]  # A specification of the API method
            if "operationId" not in oas_method:
                raise Exception(f"operationId missing in {oas_path}:{oas_http_method}")
            # print(f"{oas_http_method.upper()} {oas_path}")
            # All attributes of `method_to_add` must be defined, even if not in OAS
            method_to_add = Method(config, {
                "path": oas_path,
                "http_method": oas_http_method,
                "operation_id": oas_method["operationId"],
                "summary": dict_checked(oas_method, "summary"),
                "description": dict_checked(oas_method, "description"),
                "parameters": [
                    {
                        _["name"]: {
                            "in": dict_checked(_, "in"),
                            "description": dict_checked(_, "description"),
                            "required": dict_checked(_, "required", False),
                            "example": dict_checked(_, "example"),
                            "schema": dict_checked(_, "schema"),
                            "style": dict_checked(_, "style"),
                            "explode": dict_checked(_, "explode", False),
                        } for _ in oas_method["parameters"] if "name" in _
                    }
                ] if "parameters" in oas_method else [],
                "request_body": oas_method["requestBody"] if "requestBody" in oas_method else {},
            })

            # print(method_to_add)
            methods.append(method_to_add)

    methods.sort(key=lambda _: f"{_.class_name}/{_.method_name}")

    return methods


def gen_header(config, methods):
    # A set of unique class names
    class_set = sorted(set(_.class_name for _ in methods))
    classes = {}
    invalid_classes = {}
    for class_name in class_set:
        # All methods in the class
        methods_of_class = [_ for _ in methods if _.class_name == class_name]
        if len(methods_of_class): # Show always be True
            path_of_class = methods_of_class[0].class_path
            for _ in methods:
                if _.class_name == class_name and \
                    _.class_path != path_of_class:
                    print_error(f"{class_name}.{_.method_name}() on \"{_.class_path}\" instead of \"{path_of_class}\"")
                    if class_name not in invalid_classes:
                        invalid_classes[class_name] = set([path_of_class])
                    invalid_classes[class_name].add(_.class_path)
        if invalid_classes == {}:
            method_names_of_class = [_.method_name for _ in methods_of_class]
            classes.update({
                class_name: {
                    "methods": method_names_of_class,
                    "count": len(methods_of_class),
                }
            })

    if invalid_classes:
        # classes is empty
        print_error()
        print_error(f"Error:")
        for _ in invalid_classes:
            print_error(f"  Multiple class paths in {_}: {', '.join(invalid_classes[_])}")
        print_error()
        print_error(f"Possibly due to invalid resource consolidation in:")
        print_error(f"  config.naming[\"class_name\"] == \"{config.naming['class_name']}\"")
        exit(1)

    print_line(f"# PyLapi API generated by {main_basename}")
    print_line(f"#")
    print_line(f"# API Class: {config.api_class_name}")
    print_line(f"# {len(classes)} Resource Classes:")
    for _ in classes:
        print_line(f"#      {_}: {classes[_]['count']} native methods")
    print_line(f"# Total: {len(methods)} native methods")
    print_line()

    if debug:
        # Output OpenAI analysis then exit
        print_line(f"#")
        ii = 0
        for method in methods:
            ii += 1
            print_line(f"#{ii:4}. {method.class_name}:{method.method_name}(): {method.http_method} {method.path}")
        exit(0)

    return classes


def gen_api_class(config):
    global snippets
    global code_rewrite_lines

    api_auth_type = "Bearer"
    try:
        api_auth_type = config.api_auth_type
    except:
        config.api_auth_type = api_auth_type

    intro_line, code_lines, co = rewrite_me("@", "Custom opening")
    print_line(intro_line)
    print_line(code_lines)

    print_line("from pylapi import PyLapi, PyLapiError")
    print_line()

    intro_line, code_lines, co = rewrite_me(f"{config.api_class_name}.@", f"Custom API class: {config.api_class_name}(PyLapi)")
    print_line(intro_line)
    print_line(f"{co}class {config.api_class_name}(PyLapi):")
    print_line(f"{co}    def __init__(self, *args, **kwargs) -> None:")
    print_line(f"{co}        super().__init__(*args, **kwargs)")
    print_line(f"{co}        self.api_url = \"{config.api_url}\"")
    print_line(f"{co}        self.api_auth_type = \"{config.api_auth_type}\"")
    print_line(code_lines)
    print_line()


def print_class(config, method, classes, resource_class_args_str):
    print_line()

    intro_line, code_lines, co = rewrite_me(f"{method.class_name}.@", f"Custom resource class: {method.class_name}({config.api_class_name})")
    print_line(intro_line)
    print_line(f"{co}@{config.api_class_name}.resource_class(\"{method.resource_name}\", \"{method.class_path}\"{resource_class_args_str})")
    print_line(f"{co}class {method.class_name}({config.api_class_name}):")
    print_line(code_lines)

    print_line(f"# To instantiate: {config.api_class_name}.resource(\"{method.resource_name}\")")
    print_line(f"# Number of native methods: {classes[method.class_name]['count']}")
    for _ in classes[method.class_name]["methods"]:
        print_line(f"#     {_}")


def print_method(config, method, resource_method_args_str):
    print_line()

    route_var_names = re.findall(r"{([a-zA-Z_-]([0-9a-zA-Z_-])*)}", method.resource_path)
    route_var_names = [_[0] + "=..." for _ in route_var_names]
    route_var_names.append("...")
    route_args_text = ", ".join(route_var_names)

    intro_line, code_lines, co = rewrite_me(f"{method.class_name}.{method.method_name}", f"Custom resource method: {method.class_name}.{method.method_name}()")
    print_line(intro_line)
    print_line(f"    {co}@{config.api_class_name}.resource_method(\"{method.resource_path}\", http_method=\"{method.http_method}\"{resource_method_args_str})")
    print_line(f"    {co}def {method.method_name}(self): pass")
    print_line(code_lines)
    print_line(f"    # To call: {config.api_class_name}.resource(\"{method.resource_name}\").{method.method_name}({route_args_text})")
    print_line(f"    # Request: {method.http_method} {config.api_url}{method.api_path}")
    print_line()


def print_guide(method):
    def _multiline_trim(ml, n):
        _ml = ml
        _ml = re.sub(r"\n+$", "", _ml)
        _ml = re.sub(r"\n", "\n    #" + " " * n, _ml)
        _ml = re.sub(r" +\n", "\n", _ml)
        return _ml

    def _deref(data: dict, oas_spec: dict):
        if type(data) == dict:
            if len(data) != 1 or list(data.keys())[0] != "$ref":
                return {_: _deref(data[_], oas_spec) for _ in data}
            else:
                ref = data[list(data.keys())[0]]
                ref = re.sub(r"^#", "$", ref)
                ref = re.sub(r"/", ".", ref)
                return _deref(MagicO(oas_spec)[ref], oas_spec)
        elif type(data) == list:
            return [_deref(_, oas_spec) for _ in data]
        else:
            return data

    if "summary" in guide_attrs:
        try:
            summary = None
            if method.summary:
                summary = f"Summary: {method.summary}"
                summary = _multiline_trim(summary, 3)
        except:
            pass
        else:
            if summary != None:
                print_line(f"    # {summary}")

    if "description" in guide_attrs:
        try:
            description = None
            if method.description:
                description = f"Description:\n{method.description}"
                description = _multiline_trim(description, 3)
        except:
            pass
        else:
            if description != None:
                print_line(f"    # {description}")

    if "parameters" in guide_attrs:
        try:
            parameters = None
            if len(method.parameters) > 0 and method.parameters != [{}]:
                parameters = method.parameters.copy()
                if "ref" in guide_attrs:
                    parameters = _deref(parameters, oas_spec)
                parameters = "Parameters:\n" + re.sub(r"^-", " ", yaml.dump(parameters, indent=2, sort_keys=False))
                parameters = _multiline_trim(parameters, 1)
        except:
            pass
        else:
            if parameters != None:
                print_line(f"    #")
                print_line(f"    # {parameters}")

    if "request_body" in guide_attrs:
        try:
            rb_desc = None
            rb_content = None
            if method.request_body != {}:
                if "description" in method.request_body:
                    rb_desc = "  description: " + method.request_body['description']
                    rb_desc = _multiline_trim(rb_desc, 5)
                if "content" in method.request_body:
                    rb_content = method.request_body['content'].copy()
                    if "ref" in guide_attrs:
                        rb_content = _deref(rb_content, oas_spec)
                    rb_content = "  content:\n" + yaml.dump(rb_content, indent=2, sort_keys=False)
                    rb_content = _multiline_trim(rb_content, 5)
        except:
            pass
        else:
            if rb_desc != None or rb_content != None:
                print_line(f"    #")
                print_line(f"    # Request Body:")
                if rb_desc != None:
                    print_line(f"    # {rb_desc}")
                if rb_content != None:
                    print_line(f"    # {rb_content}")


def gen_resource_classes(config, methods, classes):
    resource_class_args_str = ""
    try:
        for resource_class_arg in config.resource_class_args:
            val = config.resource_class_args[resource_class_arg]
            if type(val) == str:
                val = f'"{val}"'
            resource_class_args_str += f", {resource_class_arg}={val}"
    except:
        pass

    resource_method_args_str = ""
    try:
        for resource_method_arg in config.resource_method_args:
            val = config.resource_method_args[resource_method_arg]
            if type(val) == str:
                val = f'"{val}"'
            resource_method_args_str += f", {resource_method_arg}={val}"
    except:
        pass

    # `resource_class` - change of first path item
    # `resource_method` - on every path, method being operation_id
    last_class_name = None
    num_methods = 0
    for method in methods:
        this_class_name = method.class_name
        if this_class_name != last_class_name:
            if last_class_name != None:
                # New custom methods of the class
                if snippets[last_class_name]:
                    # `snippets` can be changed in rewrite_me()
                    for new_method in snippets[last_class_name].copy():
                        intro_line, code_lines, co = rewrite_me(f"{last_class_name}.{new_method}", f"Custom new resource method: {last_class_name}.{new_method}()")
                        print_line(intro_line)
                        print_line(code_lines)
                        num_methods += 1
                if num_methods == 0:
                    print_line("    pass")
                    print_line()
            last_class_name = this_class_name
            num_methods = 0
            print_class(config, method, classes, resource_class_args_str)
        num_methods += 1
        print_method(config, method, resource_method_args_str)
        print_guide(method)
        # print_line()

    if last_class_name and num_methods == 0:
        print_line("    pass")

    # Handle left-over snippet classes
    snippets_flats = []
    snippets_dict = snippets.to_dict()
    for snippet_class in snippets_dict:
        for snippet_code in snippets_dict[snippet_class]:
            snippets_flats.append(f"{snippet_class}.{snippet_code}")
    # print(snippets_flats)

    if len(snippets_flats):
        print_line()
        print_line()
        print_line("# Custom new resource classes")
        print_line()
        for snippets_name in snippets_flats:
            print_line("\n".join(code_rewrite_lines[slice(*snippets[snippets_name])]))


def main():
    global debug
    global output_py
    global oas_spec
    global guide_attrs
    global config_file

    ############################################################
    #
    # Arguments and configuration
    #

    # Getopt - cannot load config for defaults until after getopt
    try:
        opts, args = getopt(sys.argv[1:], "ho:g:td", ["help", "output=", "guide=", "template", "debug"])
    except GetoptError as err:
        print_error(err)
        usage(2)

    for _o, _a in opts:
        if _o in ("-h", "--help"):
            usage()
        elif _o in ("-o", "--output"):
            if _a == "-":
                output_py = sys.stdout
            else:
                output_py_name = _a
                output_py = open(_a, "w")
        elif _o in ("-g", "--guide"):
            guide_attrs = set(_a.split(","))
            unknown_specs = []
            for _ in guide_attrs:
                if _ not in valid_guide_attrs:
                    unknown_specs.append(_)
            if unknown_specs != []:
                print_error(f"Unknown guide options: {', '.join(unknown_specs)}")
                usage(2)
            if "all" in guide_attrs:
                # Cannot copy over guide_attrs as "ref" may be in
                guide_attrs = guide_attrs.union(all_guide_attrs)
                guide_attrs.remove("all")
        elif _o in ("-t", "--template"):
            import inspect
            import autogen_template
            print(inspect.getsource(autogen_template), end='')
            exit(0)
        elif _o in ("-d", "--debug"):
            debug = True
        else:
            print_error("Invalid option: {_o}")
            usage(2)

    if len(args) < 1 or len(args) > 2:
        usage(1)

    # Load config file
    config_file = args[0]
    config_dirname = os.path.dirname(config_file)
    config_module_name = re.sub(r"\.py$", "", os.path.basename(config_file))
    sys.path.append(config_dirname)
    import importlib
    config = importlib.import_module(config_module_name)

    # Process defaults
    if output_py == None:
        try:
            output_py_name = config.output_py_name
            if output_py_name[0] == "." and config_dirname:
                # Relative path
                output_py_name = f"{config_dirname}/{output_py_name}"
            output_py = open(output_py_name, "w")
        except:
            output_py = sys.stdout

    if guide_attrs == None:
        try:
            guide_attrs = config.guide_attrs
        except:
            guide_attrs = set()

    # Process OAS file
    oas_file_name = f"{config_module_name}.json"  # Default OpenAI definition
    if len(args) >= 2:
        # openapi.json specified
        oas_file_name = args[0]
    else:
        try:
            # Use config.oas if defined
            oas_file_name = config.oas_file_name
            if oas_file_name[0] == "." and config_dirname:
                # Relative path
                oas_file_name = f"{config_dirname}/{oas_file_name}"
        except:
            # Use default
            pass

    # Process Code Rewrite file
    code_rewrite_file_name = ""
    try:
        # Use config.oas if defined
        code_rewrite_file_name = config.code_rewrite_file_name
        if code_rewrite_file_name[0] == "." and config_dirname:
            # Relative path
            code_rewrite_file_name = f"{code_rewrite_file_name}/{oas_file_name}"
    except:
        # Use default
        pass


    ############################################################
    #
    # Generate the API SDK
    #

    oas_spec = get_oas_spec(oas_file_name)
    set_config(config, oas_spec)
    get_code_rewrite(config, code_rewrite_file_name)
    methods = get_methods(config, oas_spec["paths"])
    classes = gen_header(config, methods)
    gen_api_class(config)
    gen_resource_classes(config, methods, classes)

    if output_py_name:
        code_rewrite_text = f", merged with {code_rewrite_file_name}," if code_rewrite_file_name else ""
        print(f"{config.api_class_name} generated{code_rewrite_text} and saved in {output_py_name}")

if __name__ == "__main__":
    main()
