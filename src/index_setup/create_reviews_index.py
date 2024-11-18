from typing import List, Tuple

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
                                                   SemanticConfiguration,
                                                   SemanticPrioritizedFields,
                                                   SemanticField)

from src.utils.common_utils import create_an_index, get_custom_analyzer

if __name__ == "__main__":

    fields: List[SearchableField] = [

        # "searchable": False by default in SimpleField
        SimpleField(
            name="id",
            searchable = False,
            retrievable=True,
            type=SearchFieldDataType.String,
            key=True),

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
                        )
    ]


    # add custom analyzers
    my_custom_lucene_analyzer = LuceneStandardAnalyzer(
        name="funny_standard_lucene",
        max_token_length=300)


    # semantic search
    semantic_content_field = SemanticField(field_name="ReviewText")

    semantic_prioritized_fields = SemanticPrioritizedFields(content_fields=[semantic_content_field])

    semantic_configuration = SemanticConfiguration(name="my_semantic_configuration",
                                                   prioritized_fields=semantic_prioritized_fields)
    my_semantic_search = SemanticSearch(default_configuration_name="my_semantic_configuration",
                                        configurations=[semantic_configuration])


    # custom_analyzer: Tuple[PatternTokenizer,StopwordsTokenFilter,PatternReplaceCharFilter,CustomAnalyzer] = get_custom_analyzer()


    create_an_index("fowlart_product_review_hybrid",
                    fields,
                    #[my_custom_lucene_analyzer],
                    semantic_search=my_semantic_search)