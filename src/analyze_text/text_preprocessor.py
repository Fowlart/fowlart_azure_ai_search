from os import DirEntry

from azure.ai.textanalytics import ExtractKeyPhrasesResult

from utils.common_utils import get_text_analytics_client
import os
from utils.common_utils import bcolors
import re
from pathlib import Path

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
                # todo: here we can use Aure text tokenization
                processed_line = self.__remove_empty_lines(self.__remove_punctuation(line))

                if processed_line !="":
                    self.processed_lines.append(processed_line)

        print(self.processed_lines)

        self.__write_list_to_file(
            strings=self.processed_lines,
            file_name=dir_entry.name,
            file_path=dir_entry.path,
            new_folder_name="step-0-clean-text")

        self.__extract_key_phrases(dir_entry=dir_entry)

        self.processed_lines.clear()


    #[BEGIN] key_phrases
    # todo: make sure not to break line by words
    def __chuck_lines_by_chars_qty(self, chars_qty: int) -> list[str]:

        result: list[str] = []
        cline = ""
        for line in self.processed_lines:
            if len(cline)<=chars_qty:
                cline = cline + line + os.linesep
            else:
                result.append(cline[:chars_qty])
                result.append(cline[chars_qty:])
                cline = ""

        return result

    def __extract_key_phrases(self, dir_entry: DirEntry):

        print(f"{bcolors.OKCYAN} Extracting keywords from a document... {bcolors.ENDC}")
        key_phrases_set = set()

        chunked_lines: list[str] = self.__chuck_lines_by_chars_qty(5120)

        extract_key_phrases_result: list[ExtractKeyPhrasesResult] = (self.text_analytics_client
                                                      .extract_key_phrases(documents=chunked_lines))

        print("[Debug] view key-phrases results from Language service: ")

        debug_key_phrases_results: list[str] = [str(res) for res in extract_key_phrases_result]

        self.__write_list_to_file(
            strings=debug_key_phrases_results,
            new_folder_name="step-1-key-phrases",
            file_name=dir_entry.name,
            file_path=dir_entry.path
            )

        for result in extract_key_phrases_result:
            for term in result.key_phrases:
                key_phrases_set.add(term)

        print("keyPhrasesSet: ")
        print(key_phrases_set)
    #[END] key_phrases

    def __write_list_to_file(self, strings: list[str],
                             new_folder_name: str,
                             file_path: str,
                             file_name: str):

        new_file_path = str(file_path.replace("docs-bucket", new_folder_name))

        new_dir_path: str = str(file_path.replace(file_name, "").replace("docs-bucket", new_folder_name))

        Path(new_dir_path).mkdir(parents=True, exist_ok=True)

        print(f"{bcolors.OKCYAN} Writing processed text to {file_path}/{file_name} {bcolors.ENDC}")

        with open(new_file_path, 'w') as file:
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
