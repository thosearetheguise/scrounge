import os

class FilesList:
    def __init__(self, base_path):
        self.base_path = base_path
        self.file_list = []
        self.build_file_list()

    def is_binary(self, path):
        with open(path, 'rb') as f:
            startbytes = f.read(1024)
            if not startbytes:
                print("Empty File")
                quit()

            if b'\x00' in startbytes:
                return True

            control_chars = b'\n\r\t\f\b'

            printable_ascii = control_chars + bytes(range(32, 127))
            non_human_readable = startbytes.translate(None, printable_ascii)

            ratio = len(non_human_readable) / len(startbytes)

            if ratio < 0.3:
                return False
            else:
                return True

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
                if not self.is_binary(file_path):
                    self.file_list.append(file_path)


