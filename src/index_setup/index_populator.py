import os
import mimetypes
import time
from utils.common_utils import get_tokens, get_search_index_client, get_search_client
from azure.search.documents.indexes._search_index_client import SearchClient
import base64
import uuid

class BaseIndexPopulator:

    def __init__(self,
                 index_name: str,
                 path_to_content_root: str):
        self.path_to_content_root = path_to_content_root
        self.search_index_client =get_search_index_client()
        self.search_client = get_search_client(index_name=index_name)
        self.index_name = index_name


    def populate_index(self) -> None:
        data = self._perform_text_file_indexing(root_dir=self.path_to_content_root)
        self._update_to_index(data=data, s_client=self.search_client)

    def _get_a_uuid(self):
        r_uuid = uuid.uuid4().int
        return str(r_uuid)


    def _update_to_index(self,
                         data: list[dict],
                         s_client: SearchClient):
        for doc in data:
            print(doc)
        upload_results = s_client.upload_documents(documents=data)
        for result in upload_results:
            print(result)


    def _add_language_label(self, path) -> str:
        # todo: make refactor of coupled code (use dependency injection framework?)
        with open(path.replace("docs-bucket", "step-1-language-detected"), 'r', encoding='utf-8', errors='ignore') as f:
            content: str = f.read()
        return content.strip()

    def _add_key_phrases(self, path) -> list[str]:
        result = []
        # todo: make refactor of coupled code (use dependency injection framework?)
        with open(path.replace("docs-bucket", "step-2-key-phrases"), 'r', encoding='utf-8', errors='ignore') as f:
            for line in f.readlines():
                result.append(line.strip())
        return result

    def _perform_text_file_indexing(self, root_dir: str) -> list[dict[str, str]]:
        """
        Retrieves index data for files within the specified root directory.

        Args:
            root_dir: The root directory to scan for files.

        Returns:
            A list of dictionaries, where each dictionary represents the metadata
            of a single file and contains the following keys:

                - metadata_storage_content_type: The MIME type of the file.
                - metadata_word_count: The number of words in the file.
                - metadata_storage_path: The full path to the file.
                - metadata_storage_last_modified: The last modification time of the file in ISO 8601 format.
                - metadata_storage_size: The size of the file in bytes.
        """
        metadata_list = []

        for root, dirs, files in os.walk(root_dir):
            for file in files:

                file_path = os.path.join(root, file)

                try:
                    # get file size
                    file_size = os.path.getsize(file_path)

                    # get last modified time
                    last_modified_timestamp = os.path.getmtime(file_path)

                    last_modified = time.strftime("%Y-%m-%d %H:%M:%S",
                                                  time.localtime(last_modified_timestamp))

                    # get MIME type
                    content_type, _ = mimetypes.guess_type(file_path)

                    content_type = content_type or "application/octet-stream"

                    # get word count
                    with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                        content: str = f.read()

                        tokens_count = len(get_tokens(content,
                                   # todo: here we need to pick up correct default
                                   # analyzer based on the  main document language
                                   "en.microsoft",
                                   self.index_name,
                                   self.search_index_client))

                    metadata = {
                        "metadata_storage_content_type": content_type,
                        "metadata_word_count": str(tokens_count),
                        "metadata_storage_path": file_path,
                        "metadata_storage_last_modified": last_modified,
                        "metadata_storage_size": str(file_size),
                        # todo: add to pydoc
                        "language": self._add_language_label(file_path),
                        "key_phrases": self._add_key_phrases(file_path),
                        "document_id": self._get_a_uuid()
                        }

                    metadata_list.append(metadata)

                except Exception as e:
                    print(f"Error processing file {file_path}: {e}")

        return metadata_list