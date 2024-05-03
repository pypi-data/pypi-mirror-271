from pluralizer import Pluralizer
import caseswitcher
import secrets
import uuid

pz = Pluralizer()

def lcase(x): return x[0].lower() + x[1:]
def lowercase(x): return str(x).lower()
def uppercase(x): return str(x).upper()
def joinify(column_name, item_list): return ','.join(i[column_name] for i in item_list)
def pluralize(x): return pz.pluralize(x)
def camel(x): return caseswitcher.to_camel(x)
def kebab(x): return caseswitcher.to_kebab(x)
def pascale(x): return caseswitcher.to_pascal(x)
def dot(x): return caseswitcher.to_dot(x)
def title(x): return caseswitcher.to_title(x)
def snake(x): return caseswitcher.to_snake(x)
def path(x): return caseswitcher.to_path(x)
def gen_uuid(): return str(uuid.uuid4())
def secret(): return secrets.token_hex(16)
def secret_complex(): return secrets.token_hex(64)
def env(env_file_name, config_key):
    try:
        with open(f'{env_file_name}.env', 'r') as file:
            for line in file:
                # Splitting each line by '=' and stripping whitespace
                key_value = line.strip().split('=', 1)
                if len(key_value) == 2:
                    key, value = key_value
                    if key.strip() == config_key:
                        return value.strip()
    except FileNotFoundError:
        print(f"The file {env_file_name}.env was not found.")
    except Exception as e:
        print(f"An error occurred: {e}")
    return None