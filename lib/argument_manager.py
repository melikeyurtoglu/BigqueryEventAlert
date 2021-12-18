import argparse


class ArgumentManager:
    _singleton = None

    def __new__(cls, *args, **kwargs):
        if not cls._singleton:
            cls._singleton = object.__new__(ArgumentManager)
            cls.__init__(cls)
        return cls._singleton

    def __init__(self):
        self.parser = argparse.ArgumentParser()
        self.parser.add_argument("--password",
                                 help="password to mail account", required=True)
        self.parser.add_argument("--query",
                                 help="query", required=False)
        self.parser.add_argument("--path",
                                 help="path to create csv file", required=False)
        self.parser.add_argument("--id",
                                 help="Build number", required=False)
        self.args = self.parser.parse_args()

    def get_arguments(self):
        return self.args
