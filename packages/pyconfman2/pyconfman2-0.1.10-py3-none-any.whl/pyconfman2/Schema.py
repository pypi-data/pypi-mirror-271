import os
import yaml

from .Exceptions import InvalidPropertyError, EmptyValueProperty, KeyExistsError

class ConfigSchema():
    properties = None
    current_idx = -1

    def __init__(self, default_schema={}, filepath=None, default_config=None) -> None:
        if type(default_schema) != dict:
            raise InvalidPropertyError
        
        self.properties = default_schema
        
        # Default Config is either: Provided or is searched for via "Config.y(a)ml" files
        if default_config:
            if os.path.isfile(default_config):
                self.load(default_config)
        elif not filepath:
            config_file = [item for item in os.listdir() if item == "config.yaml" or item == "config.yml"]
            for item in config_file:
                if os.path.getsize(item) > 0:
                    self.load(item)
                    break
        else:
            if os.path.isfile(filepath):
                self.load(filepath)
    
    def __str__(self) -> str:
        return str(self.properties)

    def __iter__(self):
        self.current_idx = -1
        return self
    
    def __next__(self):
        self.current_idx += 1
        if self.current_idx < len(self.properties):
            return self.properties[self.current_idx]
        raise StopIteration
    
    def add(self, nkey, nvalue=None, override=True) -> None:
        if type(nkey) == dict:
            if override:
                self.properties.update(nkey)
            else:
                self.properties = dict(list(nkey.items()) + list(self.properties.items())) 
        else:
            if nvalue == None:
                raise EmptyValueProperty
            self.properties[nkey] = nvalue
    
    def get(self, key, strict=False):
        try:
            return self.properties[key]
        except KeyError as e:
            if strict: raise e
    
    def remove(self, key, strict=False):
        try:
            self.properties.pop(key)
        except KeyError as e:
            if strict: raise e

    
    def load(self, filepath):
        if not os.path.exists(filepath):
            raise FileNotFoundException
        
        with open(filepath, "r") as fh:
            config = yaml.safe_load(fh)

        if not self.properties or not len(self.properties) > 1:
            self.properties = config
    
    def items(self):
        return self.properties.items()
