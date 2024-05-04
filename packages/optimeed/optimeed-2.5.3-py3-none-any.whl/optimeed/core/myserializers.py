
from .myjson import obj_to_json, json_to_obj, remove_module_tree_from_dict, get_json_module_tree_from_dict, apply_module_tree_to_dict
from abc import abstractmethod, ABCMeta
import json


class AbstractSerializer(metaclass=ABCMeta):
    @abstractmethod
    def serialize(self, item):
        """Serialize item (python object to json)"""
        pass

    @abstractmethod
    def deserialize(self, the_json):
        """Deserialize item (json to python object)"""
        pass

    @abstractmethod
    def get_header(self):
        """Will be saved as extradata with datastruct => returns dictionary"""
        pass

    @abstractmethod
    def set_header(self, the_json):
        """Will be set as extradata upon loading datastruct"""
        pass


class DefaultSerializer(AbstractSerializer):
    def serialize(self, item):
        return obj_to_json(item)

    def deserialize(self, the_json):
        return json_to_obj(the_json)

    def get_header(self):
        # Called once, will be placed in file. Return as
        return dict()

    def set_header(self, the_json):
        pass


class JSONmoduleTreeSerializer(AbstractSerializer):
    def __init__(self):
        self.json_module_tree = ''

    def serialize(self, item):
        self._set_json_module_tree(item)
        json_dict = obj_to_json(item)
        remove_module_tree_from_dict(json_dict)
        return json_dict

    def deserialize(self, the_json):
        apply_module_tree_to_dict(self.json_module_tree, the_json)
        return json_to_obj(the_json)

    def get_header(self):
        return self.json_module_tree

    def set_header(self, header):
        self.json_module_tree = header

    def _set_json_module_tree(self, item):
        if not self.json_module_tree:
            self.json_module_tree = get_json_module_tree_from_dict(obj_to_json(item))
