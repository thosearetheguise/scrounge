from .files import FilesList
from math import log2
import logging
import pprint


class Scrounger:
    def __init__(self, file_path):
        logging.basicConfig(level=logging.DEBUG)
        logging.debug("Grabbing files that will be scanned. Binary files will be skipped.")
        filelist = FilesList(file_path)
        self.in_scope_files = filelist.file_list
        logging.info("Got {0} files to scan.".format(len(self.in_scope_files)))

    # Splits up a line into it's tokens, or words, split by spaces.
    def get_line_tokens(self, line):
        line = line.strip()
        return line.split(" ")

    def show_in_scope_files(self):
        print(self.in_scope_files)

    def check_for_password_variables(self, file):
        """
        Literally searches for the word "password"
        :return:
        """

        with open(file, 'r') as file_text:
            count = 0
            for line in file_text:
                if "password" in line:
                    print("Found a potential password in line "+str(count)+" in file "+file+":")
                    print(line)
                count += 1

    def check_for_keys(self, line):
        """
        Unlike other functions, this one needs the entire line so that the elements of the private key headers
        are not split.
        Note, potential false positive if the line "-----BEGIN <KEYTYPE> PRIVATE KEY-----" is in a file without
        any actual body.
        :param line: A line of text from a file.
        :return: Boolean, true if found, false if not.
        """
        logging.info("Checking for keys.")
        key_headers = [
            "-----BEGIN RSA PRIVATE KEY-----",
            "-----BEGIN DSA PRIVATE KEY-----",
            "-----BEGIN EC PRIVATE KEY-----",
            "-----BEGIN PGP PRIVATE KEY-----"
        ]
        logging.debug("Processing line {0}".format(line))
        # The any function is a generator, it will check if any of the values in our key headers exists in the line.
        if any(key_header in line for key_header in key_headers):
            logging.info("Found key in line: {0}".format(line.strip()))
            return {
                "result": True,
                "data": line,
                "type": "key",
                "message": "Potential key found in file {0} on line {1}"
            }
        else:
            return {
                "result": False,
                "data": "",
                "message": ""
            }

    def check_for_high_entropy(self, line):
        # TODO: Key flaw, returns on the first instance of high entropy on a line.
        """
        Checks for high entropy strings in a line.
        :param line:
        :return:
        """
        logging.info("Checking for high entropy")
        words = self.get_line_tokens(line)
        logging.debug("Processing tokens for entropy: {0}".format(str(words)))
        for word in words:
            # Skip lines with no words.
            if word == '':
                return {
                    "result": False,
                    "data": "",
                    "type": "",
                    "message": "Blank line in file."
                }
            high_entropy = self.get_entropy(word)
            if high_entropy[0]:
                return {
                    "result": True,
                    "data": word,
                    "type": "High Entropy String",
                    "message": "Potential secret has been found in file {0} on line {1}. Value found: "+word
                }

        return {
            "result": False,
            "data": "",
            "type": "",
            "message": ""
        }

    def get_entropy(self, word):
        logging.debug("Getting entropy for word: {0}".format(word))
        alphabet = ''.join(set(word))
        length = len(word)
        ent = log2(len(alphabet * length))
        logging.debug("Entropy for word: {0}".format(ent))
        if ent > 6.5:
            return (True, ent)
        else:
            return (False, ent)

    def run_checks(self):
        """
        Loop through file list here.
        General approach change.
        For each file, we go line by line and run checks on each line.
        We pass the functions the line.
        :return:
        """

        checks_to_run = [
            self.check_for_keys,
            self.check_for_high_entropy
        ]

        results = []

        for file in self.in_scope_files:
            file_result = {
                "file": file,
                "results": []
            }
            logging.info("Scanning file {0} for secrets.".format(file))
            line_count = 0
            #self.check_for_password_variables(file)
            #self.check_for_rsa(file)
            # self.check_for_high_entropy(file)
            with open(file, "r") as file_text:
                for line in file_text:
                    for check in checks_to_run:
                        output = check(line)
                        if not output:
                            logging.debug("Something went wrong in file {0}".format(file))
                            logging.debug("On line {0}: {1}".format(line_count, line))
                            quit()
                        if output["result"]:
                            print(output["message"].format(file, line_count))
                            file_result["results"].append({"line_no": line_count, "line": line, "type": output["type"], "data": output["data"]})
                    line_count = line_count +1
            results.append(file_result)

        pprint.pprint(results)

