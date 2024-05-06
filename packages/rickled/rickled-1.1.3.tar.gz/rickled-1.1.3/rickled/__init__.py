from .__version__ import __version__, __date__
import os
import json
import copy
import warnings
from typing import Union, TypeVar
from io import TextIOWrapper, BytesIO
import yaml
import base64
import types
import re
import inspect
from functools import partial
import uuid
import sys
import tomli_w as tomlw

try:
    import requests
except ModuleNotFoundError as exc:
    warnings.warn(f"The module requests is not installed. This will break API calls.")

if sys.version_info < (3, 11):
    import tomli as toml
else:
    import tomllib as toml

from rickled.tools import toml_null_stripper

class ObjectRickler:
    """
    A class to convert Python objects to Rickle objects, deconstruct objects, create objects from Rickle objects.

    Notes:
        - `tuple` types are deconstructed as lists

    """
    def __init__(self):
        self.pat = re.compile(r'^( )*')

    def __destruct(self, value, name=None):
        if type(value) in (int, float, bool, str):
            return value

        if isinstance(value, list) or isinstance(value, tuple):
            new_list = list()
            for v in value:
                new_list.append(self.__destruct(v))
            return new_list

        if isinstance(value, dict):
            new_dict = dict()
            for k, v in value.items():
                new_dict.update({k : self.__destruct(v)})
            return new_dict

        if type(value) in (bytes, bytearray):
            return {
                'type': 'base64',
                'load': str(base64.b64encode(value))
            }

        if inspect.ismethod(value) or inspect.isfunction(value):
            signature = inspect.signature(value)
            args = dict()
            for k, v in dict(signature.parameters).items():
                if repr(v.default) == "<class 'inspect._empty'>":
                    default = None
                else:
                    default = v.default
                args.update({
                    k: default
                })

            if len(args) == 0:
                args = None

            source_lines = inspect.getsourcelines(value)[0]
            match = self.pat.match(source_lines[0])
            s = match.group(0)
            length = len(s)

            source = source_lines[0][length:]

            for s in source_lines[1:]:
                source = f'{source}{s[length:]}'


            return {
                'type': 'function',
                'name': name,
                'load': source,
                'args': args,
                'is_method' : inspect.ismethod(value)
            }

        return self.deconstruct(value)

    def to_rickle(self, obj, deep : bool = False, load_lambda : bool = False):
        """
        Transforms a Python object into a Rickle.

        Args:
            obj: Any initialised Python object.
            deep (bool): Internalize dictionary structures in lists (default = False).
            load_lambda (bool): Load python code as code or strings (default = False).

        Returns:
            Rickle: A constructed Rickle object.
        """
        d = self.deconstruct(obj)
        return Rickle(d, deep=deep, load_lambda=load_lambda)

    T = TypeVar('T')

    def from_rickle(self, rickle, cls: T, **args) -> T:
        """
        Takes a Rickle and initialises the class and updates attributes with the ones from the Rickle.

        Args:
            rickle (Rickle): Rickle to create from.
            cls (type): The class to initialise from.

        Returns:
            object: Initiliased `cls`.
        """
        if len(args) > 0:
            obj = cls(**args)
        else:
            obj = cls()

        for name, value in rickle.dict(True).items():
            if isinstance(value, dict) and 'type' in value.keys():
                if value['type'] == 'function':
                    _name = value.get('name', name)
                    _load = value['load']
                    _args = value.get('args', None)
                    _import = value.get('import', None)
                    f = rickle.add_function(name=_name, load=_load, args=_args, imports=_import,
                                            return_function=True, is_method=True)

                    obj.__dict__.update({_name: partial(f, obj)})
                continue
            obj.__dict__.update({name:value})

        return obj

    def deconstruct(self, obj, include_imports : bool = False, include_class_source : bool = False):
        """
        Takes (almost) any Python object and deconstructs it into a dict.

        Args:
            obj: Any object.
            include_imports (bool): Add a list of modules to import as is imported in current env (default = False).
            include_class_source (bool): Add the source of the object's class (default = False).

        Returns:
            dict: Deconstructed object in typical Rickle dictionary format.
        """
        d = dict()

        if include_class_source:
            source_lines = inspect.getsource(obj.__class__)
            d['class_source'] = {
                'type': 'class_source',
                'load' : source_lines
            }

        if include_imports:
            imports = list()

            for name, val in globals().items():
                if isinstance(val, types.ModuleType):
                    imports.append(val.__name__)

            if len(imports) > 0:
                d['python_modules'] = {
                    'type' : 'module_import',
                    'import' : imports
                }

        for name in dir(obj):
            if name.startswith('__'):
                continue
            value = getattr(obj, name)

            d[name] = self.__destruct(value, name)

        return d

    def to_yaml_string(self, obj):
        """
        Dumps the object to string.

        Args:
            obj: Any object.

        Returns:
            str: Dumped object.
        """
        d = self.deconstruct(obj)
        return yaml.safe_dump(d, None)

    def to_yaml_file(self, file_path, obj):
        """
        Dumps the object to file.

        Args:
            file_path: Filename.
            obj: Any object.
        """
        d = self.deconstruct(obj)
        with open(file_path, 'w', encoding='utf-8') as fs:
            yaml.safe_dump(d, fs)

    def to_json_string(self, obj):
        """
        Dumps the object to string.

        Args:
            obj: Any object.

        Returns:
            str: Dumped object.
        """
        d = self.deconstruct(obj)
        return json.dumps(d)

    def to_json_file(self, file_path, obj):
        """
        Dumps the object to file.

        Args:
            file_path: Filename.
            obj: Any object.
        """
        d = self.deconstruct(obj)
        with open(file_path, 'w', encoding='utf-8') as fs:
            json.dump(d, fs)

class BaseRickle:
    """
        A base class that creates internal structures from embedded structures.

        Args:
            base (str,dict,TextIOWrapper, list): String (YAML or JSON, file path to YAML/JSON file, URL), text IO stream, dict (default = None).
            deep (bool): Internalize dictionary structures in lists (default = False).
            strict (bool): Check keywords, if YAML/JSON key is Rickle keyword (or member of object) raise ValueError (default = True).
            **init_args (kw_args): Additional arguments for string replacement

        Raises:
            ValueError: If the given base object can not be handled. Also raises if YAML key is already member of Rickle.
    """
    def _iternalize(self, dictionary : dict, deep : bool, **init_args):
        for k, v in dictionary.items():
            self._check_kw(k)
            if isinstance(v, dict):
                self.__dict__.update({k: BaseRickle(base=v, deep=deep, strict=self.__strict, **init_args)})
                continue
            if isinstance(v, list) and deep:
                new_list = list()
                for i in v:
                    if isinstance(i, dict):
                        new_list.append(BaseRickle(base=i, deep=deep, strict=self.__strict, **init_args))
                    else:
                        new_list.append(i)
                self.__dict__.update({k: new_list})
                continue

            self.__dict__.update({k:v})

    def __init__(self, base : Union[dict,str,TextIOWrapper,list] = None, deep : bool = False, strict: bool = True, **init_args):
        self.__meta_info = dict()
        self.__strict = strict
        stringed = ''
        if base is None:
            return
        if isinstance(base, dict):
            self._iternalize(base, deep, **init_args)
            return

        if isinstance(base, TextIOWrapper):
            stringed = base.read()
        elif isinstance(base, list):
            for file in base:
                if os.path.isfile(file):
                    with open(file, 'r') as f:
                        stringed = f'{stringed}\n{f.read()}'

        elif os.path.isfile(base):
            with open(base, 'r') as f:
                stringed = f.read()
        elif isinstance(base, str):
            try:
                from urllib3.util import parse_url
                try:
                    parsed = parse_url(base)
                    if all([parsed.scheme, parsed.host]):
                        response = requests.get(url=base,)
                        dict_data = response.json()
                        self._iternalize(dict_data, deep, **init_args)
                        return
                except:
                    pass
            except (ImportError, ModuleNotFoundError):
                pass

            stringed = base

        if not init_args is None:
            for k, v in init_args.items():
                _k = f'_|{k}|_'
                stringed = stringed.replace(_k, json.dumps(v))

        error_list = list()
        try:
            dict_data = yaml.safe_load(stringed)
            self._iternalize(dict_data, deep, **init_args)
            return
        except Exception as exc:
            error_list.append(f"YAML: {exc}")
        try:
            dict_data = json.loads(stringed)
            self._iternalize(dict_data, deep, **init_args)
            return
        except Exception as exc:
            error_list.append(f"JSON: {exc}")
        try:
            dict_data = toml.loads(stringed)
            self._iternalize(dict_data, deep, **init_args)
            return
        except Exception as exc:
            error_list.append(f"TOML: {exc}")


        for error in error_list:
            print(error)
        raise ValueError('Base object could not be internalized, type {} not handled'.format(type(base)))

    def __repr__(self):
        keys = self.__dict__
        items = ("{}={!r}".format(k, self.__dict__[k]) for k in keys if not str(k).__contains__(self.__class__.__name__) and not str(k).endswith('__meta_info') )
        return "{}({})".format(type(self).__name__, ", ".join(items))

    def __str__(self):
        return self.to_yaml_string()

    def __eq__(self, other):
        return repr(self) == repr(other)

    def __len__(self):
        return len(self.__dict__)

    def __iter__(self):
        self.__n = 0
        return self

    def __next__(self):
        current_loop = 0
        if self.__n < len(self.__dict__):
            name = list(self.__dict__.keys())[self.__n]
            while self.__eval_name(name) and current_loop < 9:
                self.__n += 1
                current_loop += 1
                if self.__n < len(self.__dict__):
                    name = list(self.__dict__.keys())[self.__n]
                else:
                    raise StopIteration
            if self.__n < len(self.__dict__):
                obj = self.__dict__[list(self.__dict__.keys())[self.__n]]
                self.__n += 1
                return obj
            else:
                raise StopIteration
        else:
            raise StopIteration

    def __getitem__(self, key):
        if key is None:
            raise KeyError("NoneType is not a valid key type")
        if not isinstance(key, str):
            raise TypeError("Key can only be of case sensitive string type")

        return self.__dict__[key]

    def __setitem__(self, key, value):
        if key is None:
            raise KeyError("NoneType is not a valid key type")
        if not isinstance(key, str):
            raise TypeError("Key can only be of case sensitive string type")

        self.__dict__.update({key: value})

    def __delitem__(self, key):
        if key is None:
            raise KeyError("NoneType is not a valid key type")
        if not isinstance(key, str):
            raise TypeError("Key can only be of case sensitive string type")

        del self.__dict__[key]

    def __search_path(self, key, dictionary=None, parent_path=None):
        if dictionary is None:
            dictionary = self.dict()
        if parent_path is None:
            parent_path = ''
        values = list()
        if key in dictionary:
            values = [f'{parent_path}/{key}']
        for k, v in dictionary.items():
            if isinstance(v, BaseRickle):
                try:
                    value = self.__search_path(key=key, dictionary=v.dict(),  parent_path=f'{parent_path}/{k}')
                    values.extend(value)
                except StopIteration:
                    continue
            if isinstance(v, dict):
                try:
                    value = self.__search_path(key=key, dictionary=v,  parent_path=f'{parent_path}/{k}')
                    values.extend(value)
                except StopIteration:
                    continue
        if len(values) > 0:
            return values
        raise StopIteration

    def search_path(self, key : str) -> list:
        """
        Search the current Rickle for all paths that match the search key. Returns empty list if nothing is found.

        Args:
            key (str): The key to search.

        Returns:
            list: all paths found.
        """
        try:
            return self.__search_path(key=key)
        except StopIteration:
            return list()


    def __call__(self, path : str, **kwargs):
        """
        Rickle objects can be queried via a path string.

        Notes:
            '/' => root.
            '/name' => member.
            '/path/to/name?param=1' => lambda/function.
            If '?' is in path the inline parameters are used and kwargs are ignored.

        Args:
            path (str): The path as a string, down to the last mentioned node.

        Returns:
            Any: Value of node of function.
        """

        if not path.startswith('/'):
            raise KeyError('Missing root path /')
        if path == '/':
            return self

        path_list = path.split('/')

        current_node = self

        for node_name in path_list[1:]:
            if '?' in node_name:
                node_name = node_name.split('?')[0]
            current_node = current_node.get(node_name)
            if current_node is None:
                raise NameError(f'The path {path} could not be traversed')

        if '?' in path_list[-1]:
            import ast
            args_string = path_list[-1].split('?')[-1]
            args = {a.split('=')[0] : a.split('=')[1] for a in args_string.split('&')}
            type_guessed_args = dict()
            for n, v in args.items():
                v_stripped = v.strip()
                try:
                    literal = ast.literal_eval(v_stripped)
                except Exception as exc:
                    raise TypeError(f"Could not guess the parameter type, {exc}")

                if isinstance(literal, str):
                    # This is intentionally done to strip away the literal quotes
                    type_guessed_args[n] = v_stripped[1:-1]
                else:
                    type_guessed_args[n] = literal
            try:
                return current_node(**type_guessed_args)
            except Exception as exc:
                raise TypeError(f'{exc} occurred. The node in the path {path} is of type {type(current_node)} or does not match the query')

        if inspect.isfunction(current_node):
            try:
                return current_node(**kwargs)
            except Exception as exc:
                raise TypeError(f'{exc} occurred. The node in the path {path} is of type {type(current_node)} or does not match the query')

        else:
            return current_node


    def __eval_name(self, name):
        if str(name).__contains__(self.__class__.__name__) or str(name).endswith('__n'):
            return True
        else:
            return False

    def _check_kw(self, name):
        if self.__strict and name in dir(self):
            raise ValueError(f"Unable to add key '{name}', reserved keyword in Rickle. Use strict=False.")

    def _recursive_search(self, dictionary, key):
        if key in dictionary:
            return dictionary[key]
        for k, v in dictionary.items():
            if isinstance(v, BaseRickle):
                try:
                    value = self._recursive_search(v.__dict__, key)
                    return value
                except StopIteration:
                    continue
            if isinstance(v, dict):
                try:
                    value = self._recursive_search(v, key)
                    return value
                except StopIteration:
                    continue
        raise StopIteration

    def items(self):
        """
        Iterate through all key value pairs.

        Yields:
            tuple: str, object.
        """
        d = self.dict()
        for key in d.keys():
            if self.__eval_name(key):
                continue
            yield key, d[key]

    def get(self, key : str, default=None, do_recursive : bool = False):
        """
        Acts as a regular get from a dictionary but can employ a recursive search of structure and returns the first found key-value pair.

        Note:
            Document paths like '/root/to/path' can also be used. If the path can not be traversed, the default value is returned.

        Args:
            key (str): key string being searched.
            default (any): Return value if nothing is found.
            do_recursive (bool): Search recursively until first match is found (default = False).

        Returns:
            obj: value found, or None for nothing found.
        """
        try:
            if '/' in key:
                v = self(key)
                return v
            if do_recursive:
                value = self._recursive_search(self.__dict__, key)
            else:
                value = self.__dict__.get(key, default)
            return value
        except StopIteration:
            return default
        except NameError:
            return default
        except Exception as ex:
            raise ex

    def set(self, key: str, value):
        """
        As with the `get` method, this method can be used to update the inherent dictionary with new values.

        Note:
            Document paths like '/root/to/path' can also be used. If the path can not be traversed, an error is raised.

        Args:
            key (str): key string to set.
            value: Any Python like value that can be deserialised.
        """

        if '/' in key and not key.startswith('/'):
            raise KeyError('Missing root path /')
        if not '/' in key:
            key = f"/{key}"

        if key == '/':
            raise NameError('Can not set a value to self')

        path_list = key.split('/')

        current_node = self

        for node_name in path_list[1:-1]:
            current_node = current_node.get(node_name)
            if current_node is None:
                raise NameError(f'The path {key} could not be traversed')

        if '?' in path_list[-1]:
            raise KeyError(f'Function params "{path_list[-1]}" included in path!')

        current_node.__dict__.update({path_list[-1]: value})

    def remove(self, key: str):
        if '/' in key and not key.startswith('/'):
            raise KeyError('Missing root path /')
        if not '/' in key:
            key = f"/{key}"

        if key == '/':
            raise NameError('Can not remove self')

        path_list = key.split('/')

        current_node = self

        for node_name in path_list[1:-1]:
            current_node = current_node.get(node_name)
            if current_node is None:
                raise NameError(f'The path {key} could not be traversed')

        if '?' in path_list[-1]:
            raise KeyError(f'Function params "{path_list[-1]}" included in path!')

        del current_node.__dict__[path_list[-1]]


    def values(self):
        """
        Gets the higher level values of the current Rick object.

        Returns:
            list: of objects.
        """
        d = self.dict()
        keys = list(d.keys())
        objects = [d[k] for k in keys if not self.__eval_name(k)]

        return objects

    def keys(self):
        """
        Gets the higher level keys of the current Rick object.

        Returns:
            list: of keys.
        """
        d = self.dict()
        keys = list(d.keys())
        keys = [k for k in keys if not self.__eval_name(k)]

        return keys

    def dict(self, serialised : bool = False):
        """
        Deconstructs the whole object into a Python dictionary.

        Args:
            serialised (bool): Give a Python dictionary in serialised (True) form or deserialised (default = False).

        Notes:
            Functions and lambdas are always given in serialised form.

        Returns:
            dict: of object.
        """
        d = dict()
        for key, value in self.__dict__.items():
            if self.__eval_name(key) or str(key).endswith('__meta_info'):
                continue
            if isinstance(value, BaseRickle) or isinstance(value, Rickle):
                d[key] = value.dict(serialised=serialised)
            elif isinstance(value, list):
                new_list = list()
                for element in value:
                    if isinstance(element, BaseRickle):
                        new_list.append(element.dict(serialised=serialised))
                    else:
                        new_list.append(element)
                d[key] = new_list
            else:
                d[key] = value
        return d

    def has(self, key : str, deep=False) -> bool:
        """
        Checks whether the key exists in the object.

        Args:
            key (str): key string being searched.
            deep (bool): whether to search deeply (default = False).

        Returns:
            bool: if found.
        """
        if key in self.dict():
            return True
        if deep:
            try:
                self._recursive_search(self.dict(), key)
                return True
            except StopIteration:
                return False
        return False

    def to_yaml(self, output: Union[str, TextIOWrapper] = None, serialised: bool = False):
        """
        Does a self dump to a YAML file or returns as string.

        Args:
            output (str, TextIOWrapper): File path or stream (default = None).
            serialised (bool): Give a Python dictionary in serialised (True) form or deserialised (default = False).

        Notes:
            Functions and lambdas are always given in serialised form.
        """

        self_as_dict = self.dict(serialised=serialised)

        if output:
            if isinstance(output, TextIOWrapper):
                yaml.safe_dump(self_as_dict, output)
            elif isinstance(output, str):
                with open(output, 'w', encoding='utf-8') as fs:
                    yaml.safe_dump(self_as_dict, fs)
        else:
            return yaml.safe_dump(self_as_dict, None)

    def to_json(self, output: Union[str, TextIOWrapper] = None, serialised: bool = False):
        """
        Does a self dump to a JSON file or returns as string.

        Args:
            output (str, TextIOWrapper): File path or stream (default = None).
            serialised (bool): Give a Python dictionary in serialised (True) form or deserialised (default = False).

        Notes:
            Functions and lambdas are always given in serialised form.
        """
        self_as_dict = self.dict(serialised=serialised)

        if output:
            if isinstance(output, TextIOWrapper):
                json.dump(self_as_dict, output)
            elif isinstance(output, str):
                with open(output, 'w', encoding='utf-8') as fs:
                    json.dump(self_as_dict, fs)
        else:
            return json.dumps(self_as_dict)

    def to_toml(self, output: Union[str, BytesIO] = None, serialised: bool = False):
        """
        Does a self dump to a TOML file or returns as string.

        Args:
            output (str, TextIOWrapper): File path or stream (default = None).
            serialised (bool): Give a Python dictionary in serialised (True) form or deserialised (default = False).

        Notes:
            Functions and lambdas are always given in serialised form.
            IO stream "output" needs to be BytesIO object
        """

        self_as_dict = toml_null_stripper(self.dict(serialised=serialised))

        if output:
            if isinstance(output, BytesIO):
                tomlw.dump(self_as_dict, output)
            elif isinstance(output, str):
                with open(output, 'wb', encoding='utf-8') as fs:
                    tomlw.dump(self_as_dict, fs)
        else:
            return tomlw.dumps(self_as_dict)

    def to_yaml_file(self, file_path : str, serialised : bool = False):
        """
        (DEPRECATED) After version 1.5.0 this will be removed, use ``to_yaml`` instead.
        Does a self dump to a YAML file.

        Args:
            file_path (str): File path.
            serialised (bool): Give a Python dictionary in serialised (True) form or deserialised (default = False).

        Notes:
            Functions and lambdas are always given in serialised form.
        """
        self_as_dict = self.dict(serialised=serialised)
        with open(file_path, 'w', encoding='utf-8') as fs:
            yaml.safe_dump(self_as_dict, fs)

    def to_yaml_string(self, serialised : bool = False):
        """
        (DEPRECATED) After version 1.5.0 this will be removed, use ``to_yaml`` instead.
        Dumps self to YAML string.

        Args:
            serialised (bool): Give a Python dictionary in serialised (True) form or deserialised (default = False).

        Notes:
            Functions and lambdas are always given in serialised form.

        Returns:
            str: YAML representation.
        """
        self_as_dict = self.dict(serialised=serialised)
        return yaml.safe_dump(self_as_dict, None)

    def to_json_file(self, file_path: str, serialised : bool = False):
        """
        (DEPRECATED) After version 1.5.0 this will be removed, use ``to_json`` instead.
        Does a self dump to a JSON file.

        Args:
            file_path (str): File path.
            serialised (bool): Give a Python dictionary in serialised (True) form or deserialised (default = False).

        Notes:
            Functions and lambdas are always given in serialised form.
        """
        self_as_dict = self.dict(serialised=serialised)
        with open(file_path, 'w', encoding='utf-8') as fs:
            json.dump(self_as_dict, fs)

    def to_json_string(self, serialised : bool = False):
        """
        (DEPRECATED) After version 1.5.0 this will be removed, use ``to_json`` instead.
        Dumps self to YAML string.

        Args:
            serialised (bool): Give a Python dictionary in serialised (True) form or deserialised (default = False).

        Notes:
            Functions and lambdas are always given in serialised form.

        Returns:
            str: JSON representation.
        """
        self_as_dict = self.dict(serialised=serialised)
        return json.dumps(self_as_dict)

    def meta(self, name):
        """
        Get the metadata for a property.

        Args:
            name (str): The name of the property.

        Returns:
            dict: The metadata as a dict.
        """
        return self.__meta_info[name]

    def add_attr(self, name, value):
        """
        Add a new attribute member to Rick.

        Args:
            name (str): Property name.
            value (any): Value of new member.
        """
        self._check_kw(name)
        self.__dict__.update({name: value})
        self.__meta_info[name] = {'type': 'attr', 'value': value}

class Rickle(BaseRickle):
    """
        An extended version of the BasicRick that can load OS environ variables and Python functions.

        Args:
            base (str, list): String (YAML or JSON, file path to YAML/JSON file) or list of file paths, text IO stream, dict.
            deep (bool): Internalize dictionary structures in lists.
            load_lambda (bool): Load lambda as code or strings.
            strict (bool): Check keywords, if YAML/JSON key is Rickle keyword (or member of object) raise ValueError (default = True).
            **init_args (kw_args): Additional arguments for string replacement

        Raises:
            ValueError: If the given base object can not be handled. Also raises if YAML key is already member of Rickle.
    """

    def _iternalize(self, dictionary: dict, deep: bool, **init_args):
        for k, v in dictionary.items():
            self._check_kw(k) # Redundant but easier to check twice than to paste 10 times
            if isinstance(v, dict):
                if 'type' in v.keys():
                    if v['type'] == 'env':
                        self.add_env_variable(name=k,
                                              load=v['load'],
                                              default=v.get('default', None))
                        continue
                    if v['type'] == 'base64':
                        self.add_base64(name=k,
                                              load=v['load'])
                        continue
                    if v['type'] == 'module_import':
                        self.add_module_import(name=k,
                                              imports=v['import'])
                        continue
                    if v['type'] == 'from_file':
                        self.add_from_file(name=k,
                                           file_path=v['file_path'],
                                           load_as_rick=v.get('load_as_rick', False),
                                           deep=v.get('deep', False),
                                           load_lambda=v.get('load_lambda', False),
                                           is_binary=v.get('is_binary', False),
                                           encoding=v.get('encoding', 'utf-8'),
                                           hot_load=v.get('hot_load', False))
                        continue
                    if v['type'] == 'from_csv':
                        self.add_csv_file(name=k,
                                          file_path=v['file_path'],
                                          fieldnames=v.get('fieldnames', None),
                                          load_as_rick=v.get('load_as_rick', False),
                                          encoding=v.get('encoding', 'utf-8'))
                        continue
                    if v['type'] == 'api_json':
                        self.add_api_json_call(name=k,
                                               url=v['url'],
                                               http_verb=v.get('http_verb', 'GET'),
                                               headers=v.get('headers', None),
                                               params=v.get('params', None),
                                               body=v.get('body', None),
                                               load_as_rick=v.get('load_as_rick', False),
                                               load_lambda=v.get('load_lambda', False),
                                               deep=v.get('deep', False),
                                               expected_http_status=v.get('expected_http_status', 200),
                                               hot_load=v.get('hot_load', False))
                        continue
                    if v['type'] == 'html_page':
                        self.add_html_page(name=k,
                                           url=v['url'],
                                           headers=v.get('headers', None),
                                           params=v.get('params', None),
                                           expected_http_status=v.get('expected_http_status', 200),
                                           hot_load=v.get('hot_load', False))
                        continue
                    if v['type'] == 'lambda':
                        load = v['load']
                        imports = v.get('import', None)
                        safe_load = os.getenv("RICKLE_SAFE_LOAD", None)
                        if init_args and init_args['load_lambda'] and safe_load is None:
                            self.add_lambda(name=k,
                                            load=load,
                                            imports=imports)
                        else:
                            self.__dict__.update({k: v})
                        continue
                    if v['type'] == 'class_definition':
                        name = v.get('name', k)
                        attributes = v['attributes']
                        imports = v.get('import', None)
                        safe_load = os.getenv("RICKLE_SAFE_LOAD", None)
                        if init_args and init_args['load_lambda'] and safe_load is None:
                            self.add_class_definition(name=name,
                                              attributes=attributes,
                                              imports=imports)
                        else:
                            self.__dict__.update({k: v})
                        continue
                    if v['type'] == 'function':
                        name = v.get('name', k)
                        load = v['load']
                        args_dict = v.get('args', None)
                        imports = v.get('import', None)
                        is_method = v.get('is_method', False)

                        safe_load = os.getenv("RICKLE_SAFE_LOAD", None)
                        if init_args and init_args['load_lambda'] and safe_load is None:
                            self.add_function(name=name,
                                              load=load,
                                              args=args_dict,
                                              imports=imports,
                                              is_method=is_method)
                        else:
                            self.__dict__.update({k: v})
                        continue

                self.__dict__.update({k:Rickle(base=v, deep=deep, strict=self.__strict, **init_args)})
                continue
            if isinstance(v, list) and deep:
                new_list = list()
                for i in v:
                    if isinstance(i, dict):
                        new_list.append(Rickle(base=i, deep=deep, strict=self.__strict, **init_args))
                    else:
                        new_list.append(i)
                self.__dict__.update({k: new_list})
                continue
            self.__dict__.update({k: v})

    def __init__(self, base: Union[dict, str, TextIOWrapper, list] = None,
                 deep: bool = False,
                 load_lambda: bool = False,
                 strict: bool = True,
                 **init_args):
        self.__meta_info = dict()
        init_args['load_lambda'] = load_lambda
        init_args['deep'] = deep
        init_args['strict'] = strict
        self.__strict = strict
        self.__init_args = init_args
        super().__init__(base, **init_args)

    def __eval_name(self, name):
        if str(name).__contains__(self.__class__.__name__) or str(name).endswith('__n'):
            return True
        else:
            return False

    def meta(self, name):
        """
        Get the metadata for a property.

        Args:
            name (str): The name of the proprty.

        Returns:
            dict: The metadata as a dict.
        """
        return self.__meta_info[name]

    def dict(self, serialised : bool = False):
        """
        Deconstructs the whole object into a Python dictionary.

        Args:
            serialised (bool): Give a Python dictionary in serialised (True) form or deserialised (default = False).

        Notes:
            Functions and lambdas are always given in serialised form.

        Returns:
            dict: of object.
        """
        d = dict()
        for key, value in self.__dict__.items():
            if self.__eval_name(key):
                continue
            if serialised and key in self.__meta_info.keys():
                d[key] = self.__meta_info[key]
            # Revisit this at some later point
            elif key in self.__meta_info.keys() and \
                    self.__meta_info[key]['type'] in ['function', 'lambda', 'class_definition', 'module_import', 'base64']:
                # d[key] = self.__meta_info[key]
                continue
            elif key in self.__meta_info.keys() and \
                    self.__meta_info[key]['type'] in ['from_file', 'html_page', 'api_json'] and \
                    self.__meta_info[key]['hot_load']:
                # d[key] = self.__meta_info[key]
                continue
            elif isinstance(value, BaseRickle):
                d[key] = value.dict(serialised=serialised)
            elif isinstance(value, list):
                new_list = list()
                for element in value:
                    if isinstance(element, BaseRickle):
                        new_list.append(element.dict(serialised=serialised))
                    else:
                        new_list.append(element)
                d[key] = new_list
            else:
                d[key] = value
        return d

    def add_module_import(self, name, imports : list):
        """
        Add global Python module imports.

        Args:
            name: Name of import list.
            imports (list): List of strings of Python module names.

        """
        self._check_kw(name)
        for i in imports:
            if 'import' in i:
                exec(i, globals())
            else:
                exec('import {}'.format(i), globals())

        self.__meta_info[name] = {'type' : 'module_import', 'import' : imports}

    def add_function(self, name, load, args : dict = None, imports : list = None,
                     return_function : bool = False,
                     is_method : bool = False):
        """
        Add a new function to Rick.

        Args:
            name (str): Property name.
            load (str): Python code containing the function.
            args (dict): Key-value pairs of arguments with default values (default = None).
            imports (list): Python modules to import (default = None).
            return_function (bool): Add to rickle or return the function (default = False).
            is_method (bool): Indicates whether class method source includes `self` (default = False).

        Examples:
            Basic example for adding to a PickleRick:
                >> test_rick = PickleRick()

                >> load = '''
                        def tester(x, c):
                            y = x * 2 + c
                            return math.cos(y)
                        '''

                >> args = { 'x' : 0.42, 'c' : 1.7 }

                >> imports = ['math']

                >> test_rick.add_function('tester',load, args, imports)

                >> y = test_rick.tester(x=0.66, c=1.6)

        """
        if not return_function:
            self._check_kw(name)
        if imports and isinstance(imports, list):
            for i in imports:
                if 'import' in i:
                    exec(i, globals())
                else:
                    exec('import {}'.format(i), globals())
        suffix  = str(uuid.uuid4().hex)

        _load = load.replace(f'def {name}(', f'def {name}{suffix}(')
        exec(_load, globals())
        if args and isinstance(args, dict):
            if is_method:
                arg_list = ['self=self']
                arg_list_defaults = ['self=self']
            else:
                arg_list = list()
                arg_list_defaults = list()
            for arg in args.keys():
                default_value = args[arg]
                if isinstance(default_value, str):
                    arg_list_defaults.append(f"{arg}='{default_value}'")
                else:
                    arg_list_defaults.append(f"{arg}={default_value}")
                arg_list.append(f"{arg}={arg}")

            func_string = 'lambda {args_default}: {name}({args})'.format(
                args_default=','.join(arg_list_defaults),
                args=','.join(arg_list),
                name=name+suffix)
        else:
            if is_method:
                func_string = 'lambda self: {name}(self)'.format(name=name+suffix)
            else:
                func_string = 'lambda: {name}()'.format(name=name+suffix)

        if return_function:
            return eval(func_string)

        self.__dict__.update({name: eval(func_string)})
        self.__meta_info[name] = {'type' : 'function', 'name' : name, 'args' : args, 'import' : imports,
                                  'load' : load, 'is_method' : is_method}

    def add_lambda(self, name, load, imports : list = None, return_lambda : bool = False, is_method : bool = False):
        """
        Add a Python lambda to Rick.

        Args:
            name (str): Property name.
            load (str): Python code containing the lambda.
            imports (list): Python modules to import (default = None).
            return_lambda (bool): Add to rickle or return the lambda (default = False).
            is_method (bool): Add `self` param (default = False).

        Examples:
            Basic example for adding to a PickleRick:
                >> test_rick = PickleRick()

                >> load = "lambda: dd.utcnow().strftime('%Y-%m-%d')"

                >> imports = ['from datetime import datetime as dd']

                >> test_rick.add_lambda('date_str', load, imports)

                >> date_string = test_rick.date_str()
        """
        if not return_lambda:
            self._check_kw(name)
        if imports and isinstance(imports, list):
            for i in imports:
                if 'import' in i:
                    exec(i, globals())
                else:
                    exec('import {}'.format(i), globals())

        if load.startswith('lambda'):
            _load = load
        elif is_method:
                _load = f'lambda self: {load}'
        else:
            _load = f'lambda: {load}'

        if return_lambda:
            return eval(_load)

        self.__dict__.update({name: eval(_load)})
        self.__meta_info[name] = {'type' : 'lambda', 'import' : imports, 'load' : load}

    def add_env_variable(self, name, load, default = None):
        """
        Add a new OS ENVIRONMENT VARIABLE to Rick.

        Args:
            name (str): Property name.
            load (str): ENV var name.
            default (any): Default to value (default = None).
        """
        self._check_kw(name)
        self.__dict__.update({name: os.getenv(load, default)})
        self.__meta_info[name] = {'type' : 'env', 'load' : load, 'default' : default}

    def add_base64(self, name, load):
        """
        Add Base 64 encoded byte string data.

        Args:
            name (str): Property name.
            load (str): Base 64 encoded data.
        """
        self._check_kw(name)
        b = base64.b64decode(load)
        self.__dict__.update({name: b})
        self.__meta_info[name] = {'type': 'base64',
                                  'load' : load
                                  }

    def add_csv_file(self,
                     name,
                     file_path : str,
                     fieldnames : list = None,
                     load_as_rick  : bool = False,
                     encoding : str = 'utf-8'
                     ):
        """
        Adds the ability to load CSV data as lists or even a list of Ricks where the column names are the properties.

        Args:
            name (str): Property name.
            file_path (str): File path to load from.
            fieldnames (list): Column headers (default = None).
            load_as_rick (bool): If true, loads and creates Rick from source, else loads the contents as text (default = False).
            encoding (str): If text, encoding can be specified (default = 'utf-8').

        """
        self._check_kw(name)
        import csv
        with open(file_path, 'r', encoding=encoding) as file:
            dialect = csv.Sniffer().sniff(file.read(1024))
            file.seek(0)
            l = list()

            if load_as_rick:
                csv_file = csv.DictReader(file, fieldnames=fieldnames, dialect=dialect)

                for row in csv_file:
                    l.append(dict(row))

                self._iternalize({name: l}, deep=True)
            elif not fieldnames is None:

                columns = {c : list() for c in fieldnames}

                csv_file = csv.DictReader(file, fieldnames=fieldnames, dialect=dialect)

                for row in csv_file:
                    for k,v in row.items():
                        columns[k].append(v)

                self._iternalize({name: columns}, deep=False)
            else:
                csv_file = csv.reader(file, dialect=dialect)

                for row in csv_file:
                    l.append(row)

                self.__dict__.update({name: l})

        self.__meta_info[name] = {'type': 'from_csv',
                                  'file_path': file_path,
                                  'load_as_rick': load_as_rick,
                                  'fieldnames' : fieldnames,
                                  'encoding': encoding
                                  }

    def add_dataframe(self):
        # Implement later
        # self._check_kw(name)
        raise NotImplementedError()

    def _load_from_file(self,
                      file_path: str,
                      load_as_rick: bool = False,
                      deep: bool = False,
                      load_lambda: bool = False,
                      is_binary: bool = False,
                      encoding: str = 'utf-8'):
        if load_as_rick and not is_binary:
            args = copy.copy(self.__init_args)
            args['load_lambda'] = load_lambda
            args['deep'] = deep
            return Rickle(file_path, **args)
        else:
            if is_binary:
                with open(file_path, 'rb') as fn:
                    return fn.read()
            else:
                with open(file_path, 'r', encoding=encoding) as fn:
                    return fn.read()

    def add_from_file(self, name,
                      file_path : str,
                      load_as_rick : bool = False,
                      deep : bool = False,
                      load_lambda : bool = False,
                      is_binary : bool = False,
                      encoding : str = 'utf-8',
                      hot_load : bool = False):
        """
        Adds the ability to further load Ricks from other YAML or JSON files, or alternatively load a text file.
        This opens up dynamic possibility, but with that it also opens up extreme security vulnerabilities.
        Only ever load files from trusted sources.
        **Important note: Even with ``deep`` and ``load_lambda`` set to False, further file or API calls could be found within the source that loads lambda functions.**
        **Important note: Be careful to never self-reference a file, i.e. don't load the same file from within itself to avoid infinte looping.**

        Args:
            name (str): Property name.
            file_path (str): File path to load from.
            load_as_rick (bool): If true, loads and creates Rick from source, else loads the contents as text (default = False).
            deep (bool): Internalize dictionary structures in lists (default = False).
            load_lambda (bool): Load lambda as code or strings (default = False).
            is_binary (bool): If the file is a binary file (default = False).
            encoding (str): If text, encoding can be specified (default = 'utf-8').
            hot_load (bool): Load the data on calling or load it only once on start (cold) (default = False).
        """
        self._check_kw(name)
        if hot_load:
            _load = f"""lambda self=self: self._load_from_file(file_path='{file_path}',
                                          load_as_rick={load_as_rick},
                                          deep={deep},
                                          load_lambda={load_lambda},
                                          is_binary={is_binary},
                                          encoding='{encoding}')"""

            self.__dict__.update({name: eval(_load)})
        else:
            result = self._load_from_file(file_path=file_path,
                                          load_as_rick=load_as_rick,
                                          deep=deep,
                                          load_lambda=load_lambda,
                                          is_binary=is_binary,
                                          encoding=encoding)

            self.__dict__.update({name: result})

        self.__meta_info[name] = {'type': 'from_file',
                                  'file_path' : file_path,
                                  'load_as_rick' : load_as_rick,
                                  'deep' : deep,
                                  'load_lambda' : load_lambda,
                                  'is_binary' : is_binary,
                                  'encoding' : encoding,
                                  'hot_load' : hot_load
                                  }

    def _load_html_page(self,
                      url : str,
                      headers : dict = None,
                      params : dict = None,
                      expected_http_status : int = 200):
        r = requests.get(url=url, params=params, headers=headers)

        if r.status_code == expected_http_status:
            return r.text
        else:
            raise ValueError(f'Unexpected HTTP status code in response {r.status_code}')

    def add_html_page(self,
                      name,
                      url : str,
                      headers : dict = None,
                      params : dict = None,
                      expected_http_status : int = 200,
                      hot_load : bool = False):
        """
        Loads HTML page as property.

        Args:
            name (str): Property name.
            url (str): URL to load from.
            headers (dict): Key-value pair for headers (default = None).
            params (dict): Key-value pair for parameters (default = None).
            expected_http_status (int): Should a none 200 code be expected (default = 200).
            hot_load (bool): Load the data on calling or load it only once on start (cold) (default = False).

        """
        self._check_kw(name)
        if hot_load:
            _load = f"""lambda self=self: self._load_html_page(url='{url}',
                                          headers={headers},
                                          params={params},
                                          expected_http_status={expected_http_status})"""

            self.__dict__.update({name: eval(_load)})
        else:
            result = self._load_html_page(url=url,
                                          headers=headers,
                                          params=params,
                                          expected_http_status=expected_http_status)

            self.__dict__.update({name: result})

        self.__meta_info[name] = {'type': 'html_page',
                                  'url': url,
                                  'headers': headers,
                                  'params': params,
                                  'expected_http_status': expected_http_status,
                                  'hot_load' : hot_load
                                  }

    def add_class_definition(self, name, attributes, imports : list = None ):
        """
        Adds a class definition, with attributes such as functions and lambdas.

        Args:
            name (str): Property name.
            attributes (dict): Standard items or Rickle function definitions.
            imports (list): Python modules to import (default = None).

        """
        self._check_kw(name)
        if imports and isinstance(imports, list):
            for i in imports:
                if 'import' in i:
                    exec(i, globals())
                else:
                    exec('import {}'.format(i), globals())

        _attributes = dict()
        for k,v in attributes.items():
            if isinstance(v, dict):
                if 'type' in v.keys() and v['type'] == 'function':
                    _name = v.get('name', k)
                    load = v['load']
                    args_dict = v.get('args', None)
                    imports = v.get('import', None)
                    is_method = v.get('is_method', False)
                    _attributes[_name] = self.add_function(name=_name,load=load,args=args_dict,imports=imports,
                                                           return_function=True, is_method=is_method)
                    continue
                if 'type' in v.keys() and v['type'] == 'lambda':
                    load = v['load']
                    imports = v.get('import', None)
                    _attributes[k] = self.add_lambda(name=k, load=load, imports=imports, return_lambda=True, is_method=True)
                    continue
            _attributes[k] = v


        self.__dict__.update({name: type(name,(), _attributes)})

        self.__meta_info[name] = {'type' : 'class_definition', 'name' : name, 'import' : imports, 'attributes' : attributes}

    def _load_api_json_call(self,
                                url : str,
                                http_verb : str = 'GET',
                                headers : dict = None,
                                params : dict = None,
                                body : dict = None,
                                load_as_rick: bool = False,
                                deep : bool = False,
                                load_lambda : bool = False,
                                expected_http_status : int = 200):
        if http_verb.lower() == 'post':
            r = requests.post(url=url, data=body, headers=headers)
        else:
            r = requests.get(url=url, params=params, headers=headers)

        if r.status_code == expected_http_status:
            json_dict = r.json()
            if load_as_rick:
                args = copy.copy(self.__init_args)
                args['load_lambda'] = load_lambda
                args['deep'] = deep

                return Rickle(json_dict, **args)
            else:
                return json_dict
        else:
            raise ValueError(f'Unexpected HTTP status code in response {r.status_code}')


    def add_api_json_call(self, name,
                          url : str,
                          http_verb : str = 'GET',
                          headers : dict = None,
                          params : dict = None,
                          body : dict = None,
                          load_as_rick: bool = False,
                          deep : bool = False,
                          load_lambda : bool = False,
                          expected_http_status : int = 200,
                          hot_load : bool = False):
        """
        Load a JSON response from a URL and create a Rick from it. This opens up dynamic possibility,
        but with that it also opens up extreme security vulnerabilities. Only ever load JSON objects from trusted sources.
        **Important note: Even with ``deep`` and ``load_lambda`` set to False, further API calls could be found within the source that loads lambda functions.**
        **Important note: Be careful to never self-reference an API call, i.e. don't load the same API from within itself to avoid infinte looping.**

        Args:
            name (str): Property name.
            url (str): URL to load from.
            http_verb (str): Either 'POST' or 'GET' allowed (default = 'GET').
            headers (dict): Key-value pair for headers (default = None).
            params (dict): Key-value pair for parameters (default = None).
            body (dict): Key-value pair for data (default = None).
            load_as_rick (bool): If true, loads and creates Rick from source, else loads the contents as dictionary (default = False).
            deep (bool): Internalize dictionary structures in lists (default = False).
            load_lambda (bool): Load lambda as code or strings (default = False).
            expected_http_status (int): Should a none 200 code be expected (default = 200).
            hot_load (bool): Load the data on calling or load it only once on start (cold) (default = False).

        """
        self._check_kw(name)
        if hot_load:
            _load = f"""lambda self=self: self._load_api_json_call(url='{url}', 
                                http_verb='{http_verb}', 
                                headers={headers}, 
                                params={params}, 
                                body={body},
                                load_as_rick={load_as_rick},
                                deep={deep},
                                load_lambda={load_lambda},
                                expected_http_status={expected_http_status})"""

            self.__dict__.update({name: eval(_load)})
        else:
            result = self._load_api_json_call(url=url,
                                               http_verb=http_verb,
                                               headers=headers,
                                               params=params,
                                               body=body,
                                               load_as_rick=load_as_rick,
                                               deep=deep,
                                               load_lambda=load_lambda,
                                               expected_http_status=expected_http_status)

            self.__dict__.update({name: result})

        self.__meta_info[name] = {'type': 'api_json',
                                  'url': url,
                                  'http_verb': http_verb,
                                  'headers' : headers,
                                  'params' : params,
                                  'body' : body,
                                  'deep' : deep,
                                  'load_lambda' : load_lambda,
                                  'expected_http_status' : expected_http_status,
                                  'hot_load' : hot_load
                                  }
