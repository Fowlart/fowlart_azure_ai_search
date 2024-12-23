from collections import Counter
from os import DirEntry
from azure.ai.textanalytics import ExtractKeyPhrasesResult, DetectLanguageResult, DetectedLanguage
from utils.common_utils import get_text_analytics_client
import os
from utils.common_utils import bcolors
from pathlib import Path
import nltk

class TextPreprocessor:

    def __init__(self):
        # [BEGIN] env vars
        self.relevant_path_to_documents = r"../../resources/docs-bucket/"
        self.folder_for_clean_text = "step-0-clean-text"
        self.folder_key_phrases_debug = "key-phrases-debug"
        self.folder_language_detected = "step-1-language-detected"
        self.folder_text_chunks_debug = "text-chunks-debug"
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

    def __remove_empty_lines(self, text: str)-> str:
         return text.strip()

    def __preprocess(self, dir_entry: DirEntry):
        with (open(dir_entry.path) as file):
            for line in file.readlines():
                processed_line = self.__remove_empty_lines(line)
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
    def __chunk_by_sentences(self, chunk_size: int) -> list[str]:
        """Chunks text into segments based on sentence boundaries.
        Args:
            chunk_size: The maximum character size for each chunk.
        Returns:
            A list of strings, where each string is a chunk of text.
        """

        # download punkt sentence tokenizer if you haven't already
        nltk.data.find('tokenizers/punkt')

        text = "".join(self.processed_lines)  # Combine all lines into a single string
        sentences = nltk.sent_tokenize(text)  # Split into sentences
        chunks = []
        current_chunk = ""

        for sentence in sentences:
            if len(current_chunk) + len(sentence) + 1 <= chunk_size:  # +1 for space between sentences
                current_chunk += sentence + " "
            else:
                chunks.append(current_chunk.strip())  # Remove trailing space
                current_chunk = sentence + " "

        chunks.append(current_chunk.strip())  # Add the last chunk
        return chunks

    def __detect_language(self, docs: list[str]) -> str:
        results: list[DetectLanguageResult] = self.text_analytics_client.detect_language(documents=docs)
        iso6391_names: list[str] = [c.iso6391_name for c in [c.primary_language for c in results]]
        occurrence_count = Counter(iso6391_names)
        return occurrence_count.most_common(1)[0][0]

    def __extract_key_phrases(self, dir_entry: DirEntry):
        print(f"{bcolors.OKCYAN} Extracting keywords from a document... {bcolors.ENDC}")
        key_phrases_set = set()

        chunked_lines: list[str] = self.__chunk_by_sentences(5100)

        self.__write_list_to_file(strings=chunked_lines,
                                  new_folder_name=self.folder_text_chunks_debug,
                                  file_path=dir_entry.path,
                                  file_name=dir_entry.name)

        lang_code = self.__detect_language(docs=chunked_lines)

        self.__write_list_to_file(strings=[lang_code],
            new_folder_name=self.folder_language_detected,
            file_name=dir_entry.name,
            file_path=dir_entry.path)

        extract_key_phrases_result: list[ExtractKeyPhrasesResult] = \
        (self.text_analytics_client.extract_key_phrases(documents=chunked_lines, language=lang_code))
        debug_key_phrases_results: list[str] = [str(res) for res in extract_key_phrases_result]
        self.__write_list_to_file(strings=debug_key_phrases_results,
            new_folder_name=self.folder_key_phrases_debug,
            file_name=dir_entry.name,
            file_path=dir_entry.path)

        for result in extract_key_phrases_result:
            for term in result.key_phrases:
                key_phrases_set.add(term)

        self.__write_list_to_file(strings=key_phrases_set,
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
        print(f"{bcolors.OKCYAN} Writing processed text to {new_file_path} {bcolors.ENDC}")
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
