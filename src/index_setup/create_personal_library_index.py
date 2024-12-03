from operator import index
from re import search
from typing import List

from azure.search.documents.indexes import SearchIndexClient, SearchIndexerClient

from azure.search.documents.indexes.models import BlobIndexerParsingMode, BlobIndexerImageAction

from src.utils.common_utils import create_an_index, _get_storage_account_connection_string, get_search_indexer_client

from azure.search.documents.indexes.models import (SearchableField,
                                                   SearchFieldDataType,
                                                   SimpleField,
                                                   SearchField,
                                                   VectorSearch,
                                                   WebApiVectorizerParameters,
                                                   WebApiVectorizer,
                                                   HnswAlgorithmConfiguration,
                                                   VectorSearchProfile,
                                                   SearchIndexerDataContainer,
                                                   SearchIndexerDataSourceConnection,
                                                   SearchIndexer,
                                                   IndexingParameters,
                                                   BlobIndexerDataToExtract,
                                                   IndexingParametersConfiguration)

def create_update_data_source() -> SearchIndexerDataSourceConnection:

    container = SearchIndexerDataContainer(name="content")

    data_source_connection = SearchIndexerDataSourceConnection(
        name="fowlartaisearchstore",
        type="azureblob",
        connection_string=_get_storage_account_connection_string(),
        container=container)

    data_source: SearchIndexerDataSourceConnection = search_indexer_client.create_or_update_data_source_connection(data_source_connection)

    return data_source

def get_fields_definition() -> List[SearchableField]:

    fields_definition: List[SearchableField] = [

        SimpleField(name="id",
                    searchable=False,
                    retrievable=True,
                    type=SearchFieldDataType.String,
                    key=True),

        SearchableField(name="content",
                        type=SearchFieldDataType.String,
                        searchable=True,
                        retrievable=True,
                        filterable=False,
                        sortable=True,
                        facetable=True),

        SearchableField(name="metadata_storage_content_type",
                        type=SearchFieldDataType.String,
                        searchable=True,
                        retrievable=True,
                        filterable=False,
                        sortable=True,
                        facetable=True),

        SearchableField(name="metadata_title",
                        type=SearchFieldDataType.String,
                        searchable=True,
                        retrievable=True,
                        filterable=False,
                        sortable=True,
                        facetable=True),

        SearchableField(name="metadata_author",
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

        SearchableField(name="metadata_page_count",
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

def get_vector_search_configuration() -> VectorSearch:

    web_api_params_stub = WebApiVectorizerParameters(
        url="https://rivne-piano.com/",
        http_method="POST",
        http_headers={}
    )

    vector_search_vectorizer = WebApiVectorizer(
        vectorizer_name="my-vectorizer",
        web_api_parameters=web_api_params_stub
    )

    vector_algorythm_config = HnswAlgorithmConfiguration(
        name="my-VectorSearch-algorithm-config"
    )

    vector_search_profile = VectorSearchProfile(
        name="my-VectorSearch-profile",
        algorithm_configuration_name="my-VectorSearch-algorithm-config",
        vectorizer_name="my-vectorizer")

    my_vector_search = VectorSearch(
        profiles=[vector_search_profile],
        algorithms=[vector_algorythm_config],
        vectorizers=[vector_search_vectorizer]
    )

    return  my_vector_search


def get_index_configuration() -> IndexingParameters:
    index_params_config: IndexingParametersConfiguration = IndexingParametersConfiguration(
        query_timeout=None,
        parsing_mode=BlobIndexerParsingMode.DEFAULT,
        image_action=BlobIndexerImageAction.NONE,
        data_to_extract=BlobIndexerDataToExtract.CONTENT_AND_METADATA,
        allow_skillset_to_read_file_data=False,
        indexed_file_name_extensions=".pdf, .docx")

    indexing_params = IndexingParameters(configuration=index_params_config)

    return indexing_params


if __name__ == "__main__":

    personal_index_name = "fowlart_personal_index"

    indexer_name = "fowlart-indexer"

    fields: List[SearchableField] = get_fields_definition()

    vector_search_config: VectorSearch = get_vector_search_configuration()

    create_an_index(personal_index_name, fields_definition=fields)

    search_indexer_client: SearchIndexerClient = get_search_indexer_client()

    # [START create_indexer]
    indexer = SearchIndexer(
        name=indexer_name,
        data_source_name=create_update_data_source().name,
        target_index_name=personal_index_name,
        parameters = get_index_configuration())

    result = search_indexer_client.create_or_update_indexer(indexer)

    print(f"Created new indexer: {indexer.name}")
    # [END create_indexer]