from collections import Counter
from os import DirEntry
from azure.ai.textanalytics import ExtractKeyPhrasesResult, DetectLanguageResult, DetectedLanguage
from utils.common_utils import get_text_analytics_client
import os
from utils.common_utils import bcolors
import re
from pathlib import Path

class TextPreprocessor:

    def __init__(self):
        # [BEGIN] env vars
        self.relevant_path_to_documents = r"../../resources/docs-bucket/"
        self.folder_for_clean_text = "step-0-clean-text"
        self.folder_key_phrases_debug = "step-1-key-phrases-debug"
        self.folder_key_phrases = "step-2-key-phrases"
        self.path_to_text_bucket = f"{os.getcwd()}/{self.relevant_path_to_documents}"
        self.extension_to_consider = ".txt"
        # [END] env vars

        self.text_analytics_client = get_text_analytics_client()
        self.processed_lines: list[str] = []
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

        self.__write_list_to_file(
            strings=self.processed_lines,
            file_name=dir_entry.name,
            file_path=dir_entry.path,
            new_folder_name=self.folder_for_clean_text)

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

    def __detect_language(self, docs: list[str]) -> str:
        results: list[DetectLanguageResult] = self.text_analytics_client.detect_language(documents=docs)
        iso6391_names: list[str] = [c.iso6391_name for c in [c.primary_language for c in results]]
        occurrence_count = Counter(iso6391_names)
        return occurrence_count.most_common(1)[0][0]

    def __extract_key_phrases(self, dir_entry: DirEntry):
        print(f"{bcolors.OKCYAN} Extracting keywords from a document... {bcolors.ENDC}")
        key_phrases_set = set()
        chunked_lines: list[str] = self.__chuck_lines_by_chars_qty(5120)
        lang_code = self.__detect_language(docs=chunked_lines)
        extract_key_phrases_result: list[ExtractKeyPhrasesResult] = \
        (self.text_analytics_client.extract_key_phrases(documents=chunked_lines, language=lang_code))
        debug_key_phrases_results: list[str] = [str(res) for res in extract_key_phrases_result]
        self.__write_list_to_file(
            strings=debug_key_phrases_results,
            new_folder_name=self.folder_key_phrases_debug,
            file_name=dir_entry.name,
            file_path=dir_entry.path)

        for result in extract_key_phrases_result:
            for term in result.key_phrases:
                key_phrases_set.add(term)

        self.__write_list_to_file(
            strings=key_phrases_set,
            new_folder_name=self.folder_key_phrases,
            file_name=dir_entry.name,
            file_path=dir_entry.path)
    #[END] key_phrases

    def __write_list_to_file(self, strings: list[str] | set[str],
                             new_folder_name: str,
                             file_path: str,
                             file_name: str):

        new_file_path = str(file_path.replace("docs-bucket", new_folder_name))
        new_dir_path: str = str(file_path.replace(file_name, "").replace("docs-bucket", new_folder_name))
        Path(new_dir_path).mkdir(parents=True, exist_ok=True)
        print(f"{bcolors.OKCYAN} Writing processed text to {file_path}/{file_name} {bcolors.ENDC}")
        with open(new_file_path, 'w') as file:
            for string in strings:
                file.writelines(string + '\n')


    def preprocess_files(self):
        """
        Run the function to initialize a process of text file processing
        :return:
        """
        if len(self.unprocessed_files) == 0:
            print(f"No any files to preprocess!")
            return

        while not (self.__are_all_files_processed()):
            file = self.unprocessed_files.pop()
            print(f"{bcolors.OKBLUE} Process file with the name {file.name}... {bcolors.ENDC}")
            self.__preprocess(file)
