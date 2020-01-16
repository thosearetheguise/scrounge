import os
import logging

class FilesList:
    def __init__(self, base_path):
        logging.basicConfig(level=logging.DEBUG)
        self.base_path = base_path
        logging.debug("Scanning files in {0}".format(self.base_path))
        self.file_list = []
        self.build_file_list()


    def is_binary(self, path):
        with open(path, 'rb') as f:
            startbytes = f.read(1024)
            if not startbytes:
                logging.info("Empty file at {0}".format(path))
                quit()

            if b'\x00' in startbytes:
                logging.info("Binary file found at {0} (starts with \\x00)".format(path))
                return True

            control_chars = b'\n\r\t\f\b'

            printable_ascii = control_chars + bytes(range(32, 127))
            non_human_readable = startbytes.translate(None, printable_ascii)

            ratio = len(non_human_readable) / len(startbytes)

            if ratio < 0.3:
                return False
            else:
                logging.info("Binary file found at {0} (more than 30% of characters non printable)".format(path))
                return True


    def build_file_list(self):
        """
        Gets all files within the hierarchy of the base_path.
        Automatically filters out files that we don't think are binary.
        :return:
        """
        for base, subdirs, files in os.walk(self.base_path):

            for file in files:
                file_path = base + "/" + file
                # We want this to be false.
                if not self.is_binary(file_path):
                    self.file_list.append(file_path)


