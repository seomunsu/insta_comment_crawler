import json
import yaml
import types

from consts import crawler_consts


class YamlOption:
    def __init__(self):
        self.__load_option()

    def __load_option(self):
        with open(crawler_consts.CRAWLER_OPTION_FILE) as f:
            dictionary = yaml.safe_load(f)

        option = self.__load_json(dictionary)
        self.instagram = option.instagram
        self.collect = option.collect

    @staticmethod
    def __load_object(dictionary):
        return types.SimpleNamespace(**dictionary)

    def __load_json(self, obj):
        return json.loads(json.dumps(obj), object_hook=self.__load_object)
