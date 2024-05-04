def json_to_csharp_class(json_data, class_name="Root", parent_class_name=None):
    """
    Converts JSON data to C# classes and writes each class to a separate file.
    
    Args:
        json_data (dict): JSON data as a Python dictionary.
        class_name (str): Name of the current C# class.
        parent_class_name (str): Name of the parent C# class.
    """
    class_string = f"public class {class_name}\n"
    class_string += "{\n"

    for key, value in json_data.items():
        if isinstance(value, dict):
            nested_class_name = key.capitalize()
            class_string += f"\tpublic {nested_class_name} {key.title()} {{ get; set; }}\n"
            json_to_csharp_class(value, nested_class_name, class_name)
        elif isinstance(value, list):
            if value:
                if isinstance(value[0], dict):
                    nested_class_name = key.capitalize()
                    class_string += f"\tpublic List<{nested_class_name}> {key.title()} {{ get; set; }}\n"
                    json_to_csharp_class(value[0], nested_class_name, class_name)
                else:
                    class_string += f"\tpublic List<{_get_csharp_type(type(value[0]))}> {key.title()} {{ get; set; }}\n"
            else:
                class_string += f"\tpublic List<object> {key.title()} {{ get; set; }}\n"
        else:
            class_string += f"\tpublic {_get_csharp_type(type(value))} {key.title()} {{ get; set; }} {_get_csharp_default_value(type(value), value)}\n"

    class_string += "}\n"

    return class_string

def _get_csharp_type(py_type):
    """
    Maps Python types to equivalent C# types.
    
    Args:
        py_type (type): Python type.
    
    Returns:
        str: Equivalent C# type.
    """
    type_map = {
        int: "Int",
        float: "Float",
        str: "String",
        bool: "Bool"
    }
    return type_map.get(py_type, "object")

def _get_csharp_default_value(py_type, value):
    """
    Maps Python types to equivalent C# types.
    
    Args:
        py_type (type): Python type.
    
    Returns:
        str: Equivalent C# type.
    """
    default_value_map = {
        int: f"= {value};",
        float: f"= {value};",
        str: f'= "{value}";',
        bool: f"= {str(value).lower()};",
    }
    return default_value_map.get(py_type, f'={value};')
