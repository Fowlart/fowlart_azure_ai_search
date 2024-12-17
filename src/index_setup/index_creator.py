from typing import List
from utils.common_utils import create_an_index

from azure.search.documents.indexes.models import (
    SearchableField,
    SearchFieldDataType,
    SearchField)

class BaseIndexCreator:

    def get_base_index_name(self) -> str:
        return "fowlart-personal-documents-index"

    def get_fields_definition(self) -> List[SearchableField]:

        fields_definition: List[SearchableField] = [

            SearchField(name="document_id",
                        type=SearchFieldDataType.String,
                        key=True,
                        sortable=True,
                        filterable=True,
                        facetable=True,
                        analyzer_name="keyword"),

            SearchableField(name="metadata_storage_content_type",
                            type=SearchFieldDataType.String,
                            searchable=True,
                            retrievable=True,
                            filterable=False,
                            sortable=True,
                            facetable=True),

            SearchableField(name="metadata_language",
                            type=SearchFieldDataType.String,
                            searchable=True,
                            retrievable=True,
                            filterable=False,
                            sortable=True,
                            facetable=True),

            SearchableField(name="metadata_word_count",
                            type=SearchFieldDataType.String,
                            searchable=True,
                            retrievable=True,
                            filterable=False,
                            sortable=True,
                            facetable=True),

            SearchableField(name="metadata_storage_path",
                            type=SearchFieldDataType.String,
                            searchable=True,
                            retrievable=True,
                            filterable=True,
                            sortable=True,
                            facetable=True),

            SearchableField(name="metadata_storage_last_modified",
                            type=SearchFieldDataType.DateTimeOffset,
                            searchable=True,
                            retrievable=True,
                            filterable=True,
                            sortable=True,
                            facetable=True),

            SearchableField(name="metadata_storage_size",
                            type=SearchFieldDataType.Int64,
                            searchable=True,
                            retrievable=True,
                            filterable=True,
                            sortable=True,
                            facetable=True),

            SearchableField(name="key_phrases",
                            type=SearchFieldDataType.String,
                            searchable=True,
                            retrievable=True,
                            filterable=False,
                            sortable=False,
                            facetable=True,
                            collection=True),

            SearchableField(name="language",
                            type=SearchFieldDataType.String,
                            searchable=True,
                            retrievable=True,
                            filterable=True,
                            sortable=False,
                            facetable=True),

            # The main purpose of a custom search app is to return a link to the actual file
            SearchableField(name="url",
                            type=SearchFieldDataType.String,
                            searchable=False,
                            retrievable=True,
                            filterable=False,
                            sortable=False,
                            facetable=True),

            # This field might be the essence of the search app.
            # My content is unstructured data.To find a match within
            # unstructured data we need to vectorize the content.
            # SearchField(
            #     name="vectorized_content",
            #     collection=True,
            #     type=SearchFieldDataType.Collection(SearchFieldDataType.Single),
            #     vector_search_dimensions=1000,
            #     vector_search_profile_name="my-VectorSearch-profile"
            # )
        ]

        return fields_definition


    def create_index(self):

        create_an_index(
            index_name=self.get_base_index_name(),
            fields_definition=self.get_fields_definition()
        )

