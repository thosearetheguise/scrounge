from .files import FilesList

text = "lol"

class Scrounger:

    def __init__(self, file_path):
        filelist = FilesList(file_path)
        self.in_scope_files = filelist.file_list

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


    def check_for_rsa(self, file):
        """
        Literally searches for the RSA string.
        TODO - Do a better job of checking key length or detecting encrypted keys.
        TODO - Extract and show keys.
        :return:
        """
        with open(file, 'r') as file_text:
            count = 0
            rsa_start = False
            rsa_end = False
            for line in file_text:
                if "-----BEGIN RSA PRIVATE KEY-----" in line:
                    rsa_start = True
                if "-----END RSA PRIVATE KEY-----" in line:
                    rsa_end = True

            if rsa_start and rsa_end:
                print("Potential RSA key found in "+file)


    def run_checks(self):
        """
        Loop through file list here.
        :return:
        """
        for file in self.in_scope_files:
            self.check_for_password_variables(file)
            self.check_for_rsa(file)
