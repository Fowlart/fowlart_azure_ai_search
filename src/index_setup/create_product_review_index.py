from typing import List, Tuple

from azure.search.documents.indexes.models import WebApiVectorizer, HnswAlgorithmConfiguration
from azure.search.documents.indexes.models import (ComplexField,
                                                   TokenFilter,
                                                   CharFilter,
                                                   CustomAnalyzer,
                                                   PatternTokenizer,
                                                   StopwordsTokenFilter,
                                                   PatternReplaceCharFilter,
                                                   SimpleField,
                                                   SearchFieldDataType,
                                                   SearchableField,
                                                   LuceneStandardAnalyzer,
                                                   SemanticSearch,

                                                   VectorSearch,
                                                   VectorSearchProfile,
                                                   VectorSearchAlgorithmConfiguration,
                                                   VectorSearchVectorizer,
                                                   WebApiVectorizerParameters,

                                                   SemanticConfiguration,
                                                   SemanticPrioritizedFields,
                                                   SemanticField,
                                                   SearchIndex,
                                                   SearchField,
                                                   SearchSuggester)

from src.utils.common_utils import create_an_index, get_index_name

if __name__ == "__main__":

    fields: List[SearchableField] = [

        # "searchable": False by default in SimpleField
        SimpleField(
            name="id",
            searchable = False,
            retrievable=True,
            type=SearchFieldDataType.String,
            key=True),

        SearchableField(name="ProductTitle",
                        type=SearchFieldDataType.String,
                        searchable=True,
                        retrievable=True,
                        filterable=False,
                        sortable=False,
                        facetable=True,
                        # analyzer_name="funny_standard_lucene"
                        ),

        SimpleField(name="ReviewRating",
                        type = SearchFieldDataType.Int32,
                        searchable=False,
                        filterable=True,
                        retrievable=True,
                        sortable=True,
                        facetable=True,
                        sorted=True),


        SearchableField(name="ReviewText",
                        type=SearchFieldDataType.String,
                        searchable = True,
                        retrievable=True,
                        filterable=False,
                        sortable=False,
                        facetable=True,
                        # analyzer_name="funny_standard_lucene"
                        ),

        SearchableField(name="KeyPhrases",
                        type=SearchFieldDataType.String,
                        searchable=True,
                        retrievable=True,
                        filterable=False,
                        sortable=False,
                        facetable=True,
                        collection=True),

        SearchField(
            name="ReviewTextVector",
            collection=True,
            type=SearchFieldDataType.Collection(SearchFieldDataType.Single),
            vector_search_dimensions = 300,
            vector_search_profile_name= "my-VectorSearch-profile"
        )
    ]

    # vectorSearch
    web_api_params_stub = WebApiVectorizerParameters(
        url="https://rivne-piano.com/",
        http_method="POST",
        http_headers={}
    )

    vector_search_vectorizer = WebApiVectorizer(
        vectorizer_name="my-vectorizer",
        web_api_parameters = web_api_params_stub
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

    # add custom analyzers
    my_custom_lucene_analyzer = LuceneStandardAnalyzer(
        name="funny_standard_lucene",
        max_token_length=300)


    # semantic search
    semantic_content_field = SemanticField(field_name="ReviewText")

    semantic_key_phrases_field = SemanticField(field_name="KeyPhrases")

    semantic_prioritized_fields = SemanticPrioritizedFields(
        content_fields=[semantic_content_field],
        keywords_fields=[semantic_key_phrases_field])

    semantic_configuration = SemanticConfiguration(name="my_semantic_configuration",
                                                   prioritized_fields=semantic_prioritized_fields)

    my_semantic_search = SemanticSearch(default_configuration_name="my_semantic_configuration",
                                        configurations=[semantic_configuration])

    # custom_analyzer: Tuple[PatternTokenizer,StopwordsTokenFilter,PatternReplaceCharFilter,CustomAnalyzer] = get_custom_analyzer()


    # adding suggester
    keywords_suggester: SearchSuggester = SearchSuggester(name="keywords_suggester",
                                                 source_fields=["KeyPhrases"])

    title_suggester: SearchSuggester = SearchSuggester(name="title_suggester",
                                                          source_fields=["ProductTitle"])

    index: SearchIndex = create_an_index(
                    index_name=get_index_name(),
                    fields_definition=fields,
                    #[my_custom_lucene_analyzer],
                    semantic_search=my_semantic_search,
                    vector_search=my_vector_search,
                    suggesters=[title_suggester])

