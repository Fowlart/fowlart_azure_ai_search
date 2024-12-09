from azure.search.documents.indexes import SearchIndexClient

from src.utils.common_utils import  analyze_text, get_tokens, get_search_index_client, get_index_name

if __name__ == "__main__":

    print(get_tokens("""
    I've read the author of "War of THE worlds": cool stuff
    """, "en.lucene",get_index_name(), get_search_index_client()))

    analyze_text("""I've read the author of "War of THE worlds": cool stuff""", "en.lucene",get_index_name())

    analyze_text("""I've read the author of "War of THE worlds": cool stuff""","en.microsoft",get_index_name())

    analyze_text(r"Dog+cat>pig are!=n=", "my_custom_analyzer", get_index_name())

    analyze_text(text="""
    Це є демонстрація мовного аналізу українського тексту!
    Я хочу їсти яблука з цукром!""",
                 analyzer_name="uk.microsoft",
                 index_name=get_index_name())

    analyze_text("Could You tell me which products are the best?",
                 "funny_standard_lucene",
                 get_index_name())