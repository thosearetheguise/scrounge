import os
from binaryornot.check import is_binary

class FilesList:

    def __init__(self, base_path):
        self.base_path = base_path
        self.file_list = []
        self.build_file_list()

    def build_file_list(self):
        """
        Gets all files within the hierarchy of the base_path.
        Automatically filters out files that we don't think are binary.
        :return:
        """
        for base, subdirs, files in os.walk(self.base_path):

            for file in files:
                # We want this to be false.
                file_path = base + "/" + file
                if not is_binary(file_path):
                    self.file_list.append(file_path)

