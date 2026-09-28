import json


class JsonFile:
    def __init__(self, filepath):
        self.filepath = filepath

    def read(self):
        with open(self.filepath, 'r', encoding='utf-8') as file:
            return json.load(file)

    def save(self, data):
        with open(self.filepath, 'w', encoding='utf-8') as file:
            json.dump(data, file, ensure_ascii=False, indent=4)

    def find(self, key, value):
        data = self.read()
        return [item for item in data if item.get(key) == value]