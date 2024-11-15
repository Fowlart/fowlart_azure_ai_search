from typing import List

from azure.search.documents.indexes.models import (ComplexField,
                                                   TokenFilter,
                                                   CharFilter,
                                                   SimpleField,
                                                   SearchFieldDataType,
                                                   SearchableField,
                                                   LuceneStandardAnalyzer,
                                                   CustomAnalyzer,
                                                   PatternTokenizer,
                                                   StopwordsTokenFilter,
                                                   PatternReplaceCharFilter,
                                                   SemanticSearch,
                                                   SemanticConfiguration,
                                                   SemanticPrioritizedFields,
                                                   SemanticField)

from src.utils.common_utils import create_an_index

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
                        facetable=True),

        # SearchableField(name="ReviewLanguage",
        #                 type=SearchFieldDataType.String,
        #                 searchable=True,
        #                 retrievable=True,
        #                 filterable=True,
        #                 sortable=False,
        #                 facetable=True),

        # SearchableField(name="SentimentLabel",
        #                 type=SearchFieldDataType.String,
        #                 searchable=True,
        #                 retrievable=True,
        #                 filterable=True,
        #                 sortable=False,
        #                 facetable=True),

        # SearchableField(name="KeyPhrases",
        #                 type=SearchFieldDataType.String,
        #                 searchable=True,
        #                 retrievable=True,
        #                 filterable=True,
        #                 sortable=False,
        #                 facetable=True,
        #                 collection=True)
    ]


    # add custom analyzers

    my_custom_lucene_analyzer = LuceneStandardAnalyzer(
        name="funny_standard_lucene",
        max_token_length=255,
        stopwords=["dog","pig","cat"])


    pattern_tokenizer = PatternTokenizer(pattern=r"\W+",name="my_pattern_tokenizer")
    token_filter = StopwordsTokenFilter(name="my_token_filter", stopwords=["Dog","Cat","Pig"],ignore_case=True)
    char_filter = PatternReplaceCharFilter(name="my_char_filter",pattern=r"=n=",replacement="<new_line>")


    my_custom_analyzer = CustomAnalyzer(name="my_custom_analyzer",
                                        tokenizer_name="my_pattern_tokenizer",
                                        token_filters=["my_token_filter"],
                                        char_filters=["my_char_filter"])






    # semantic search
    semantic_content_field = SemanticField(field_name="ReviewText")

    semantic_prioritized_fields = SemanticPrioritizedFields(content_fields=[semantic_content_field])


    semantic_configuration = SemanticConfiguration(name="my_semantic_configuration",
                                                   prioritized_fields=semantic_prioritized_fields)

    my_semantic_search = SemanticSearch(default_configuration_name="my_semantic_configuration",
                                        configurations=[semantic_configuration])


    create_an_index("fowlart_product_review_hybrid",
                    fields,
                    [my_custom_lucene_analyzer, my_custom_analyzer],
                    [pattern_tokenizer],
                    [token_filter],
                    [char_filter],
                    semantic_search=my_semantic_search)