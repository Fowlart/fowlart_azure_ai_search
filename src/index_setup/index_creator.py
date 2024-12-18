from typing import List

from azure.search.documents.indexes.models import (SemanticField,
                                                   SemanticPrioritizedFields,
                                                   SemanticConfiguration,
                                                   SemanticSearch)

from utils.common_utils import create_an_index

from azure.search.documents.indexes.models import (
    SearchableField,
    SearchFieldDataType,
    SearchField)

class BaseIndexCreator:

    def get_semantic_search_configuration(self) -> SemanticSearch:

        semantic_key_phrases_field = SemanticField(field_name="key_phrases")

        # todo: there is no notion of a content field inside the index, but that might change.
        #   we can pull the first n sentences from the text or, for example, use LLM to summarize.
        semantic_content_field = SemanticField(field_name="_")

        semantic_prioritized_fields = SemanticPrioritizedFields(

        #content_fields=[semantic_content_field],

            keywords_fields=[semantic_key_phrases_field])

        semantic_configuration = SemanticConfiguration(name="my_semantic_configuration",
                                                       prioritized_fields=semantic_prioritized_fields)

        my_semantic_search = SemanticSearch(default_configuration_name="my_semantic_configuration",
                                            configurations=[semantic_configuration])

        return my_semantic_search

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

            #todo: vectorize the content.
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
            fields_definition=self.get_fields_definition(),
            semantic_search=self.get_semantic_search_configuration()
        )

