from os import DirEntry
from utils.common_utils import get_text_analytics_client
import os
from utils.common_utils import bcolors
import re

class TextPreprocessor:

    def __init__(self):
        self.text_analytics_client = get_text_analytics_client()
        self.processed_lines: list[str] = []
        self.path_to_text_bucket = f"{os.getcwd()}/../../resources/docs-bucket/"
        self.path_to_output_folder = f"{os.getcwd()}/../../resources/docs-output/"
        self.extension_to_consider = ".txt"
        self.unprocessed_files: list[os.DirEntry] = []
        folder = os.scandir(self.path_to_text_bucket)
        for dir_entry in folder:
            if dir_entry.is_file() & dir_entry.name.endswith(self.extension_to_consider):
                print(f"located: {bcolors.OKGREEN} {dir_entry.name} {bcolors.ENDC}")
                self.unprocessed_files.append(dir_entry)

    def __are_all_files_processed(self) -> bool:
        return len(self.unprocessed_files) == 0

    def __remove_punctuation(self, text: str) -> str:
        return re.sub(r'[^\w\s]', '', text)

    def __remove_empty_lines(self, text: str)-> str:
         return re.sub(r"[^a-zA-Z0-9 ]", "", text.strip())

    def __remove_empty_sep_lines(self, text: str)-> str:
         if (text == os.linesep) or (text == "\n"):
             return "BA"
         return text

    def __preprocess(self, dir_entry: DirEntry):
        with (open(dir_entry.path) as file):
            for line in file.readlines():
                processed_line = self.__remove_empty_lines(self.__remove_punctuation(line))
                if processed_line !="":
                    self.processed_lines.append(processed_line)
        print(self.processed_lines)
        new_file_name = str(dir_entry.path.replace("docs-bucket", "processed-docs-bucket-temp"))
        print(f"{bcolors.OKCYAN} Writing processed text to {new_file_name} {bcolors.ENDC}")
        self.__write_list_to_file(self.processed_lines, new_file_name)
        self.__extract_key_phrases()
        self.processed_lines.clear()

    # todo: make smart key-phrases extraction, to summarize document
    def __extract_key_phrases(self):
        print(f"{bcolors.OKCYAN} Extracting keywords from a document... {bcolors.ENDC}")
        for line in self.processed_lines:
            print(self.text_analytics_client.extract_key_phrases([line]))

    # todo: create folder if not exists
    def __write_list_to_file(self, strings: list[str], filename: str):
        with open(filename, 'w') as file:
            for string in strings:
                file.write(string + '\n')


    def preprocess_files(self):
        if len(self.unprocessed_files) == 0:
            print(f"No any files to preprocess!")
            return

        while not (self.__are_all_files_processed()):
            file = self.unprocessed_files.pop()
            print(f"{bcolors.OKBLUE} Process file with the name {file.name}... {bcolors.ENDC}")
            self.__preprocess(file)


