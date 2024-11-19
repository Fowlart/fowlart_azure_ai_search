from azure.search.documents import SearchClient, SearchItemPaged
from azure.search.documents.models import QueryCaptionType, QueryAnswerType

from src.utils.common_utils import get_search_client
from src.utils.common_utils import bcolors as color


def print_search_result(search_result_iterator):

    if search_result_iterator.get_answers():
        print(f"{color.HEADER}Found direct answers:{color.ENDC}")
        print(color.OKGREEN)
        for answ in search_result_iterator.get_answers():
            print(answ)
    else:
        print("No answer results!")
    print(color.ENDC)

    for x in search_result_iterator:
        print(f"{color.HEADER}Search result:{color.ENDC}")
        print(color.OKCYAN)
        print(x)
        print(color.ENDC)
        if x.get('@search.captions'):
            print(f"{color.HEADER}Caption from semantic search results:{color.ENDC}")
            for caption in x.get('@search.captions'):
                print(color.OKGREEN)
                print(caption)
                print(color.ENDC)


# goes to analyzer
def search_by_key_phrases(client: SearchClient,
                          key_phrases: list[str]):



    quoted_key_phrases = [f"'{e}'" for e in key_phrases]
    full_search_query = " ".join(quoted_key_phrases)
    full_search_query = f"KeyPhrases:({full_search_query})"

    print(f"Applied search with the query {color.OKCYAN} {full_search_query} {color.ENDC}...")
    print(color.ENDC)
    result: SearchItemPaged[dict] = client.search(
        search_text=full_search_query,
        include_total_count=True,
        search_mode="any",
        query_type="full",
        scoring_statistics="global")

    print(f"results number: {result.get_count()}")
    print_search_result(result)


def simple_search(client: SearchClient, text: str):
    print(f"Applied simple search with the query {color.OKCYAN} {text} {color.ENDC}...")

    result: SearchItemPaged[dict] = client.search(
        search_text=text,
        include_total_count=True,
        highlight_fields="ReviewText",
        query_type="simple",
        scoring_statistics="global")

    print(f"results number: {result.get_count()}")

    print_search_result(result)


def semantic_search(client: SearchClient,
                    text: str):
    print(f"Applied semantic search with the query {color.OKCYAN} {text} {color.ENDC}...")

    result: SearchItemPaged[dict] = client.search(
        search_text=text,
        semantic_query=text,
        include_total_count=True,
        highlight_fields="ReviewText",
        query_type="semantic",
        semantic_configuration_name="my_semantic_configuration",
        scoring_statistics="global",
        query_caption=QueryCaptionType.EXTRACTIVE,
        query_answer=QueryAnswerType.EXTRACTIVE

    )

    print(f"results number: {result.get_count()}")

    print_search_result(result)


# goes to analyzer
def all_terms_are_present(client: SearchClient,
                          terms: list[str]):
    search_prefix = "ReviewText:"
    modified_terms = [search_prefix + s for s in terms]
    full_search_query = " AND ".join(modified_terms)
    print(f"Applied search with the query {color.OKCYAN} {full_search_query} {color.ENDC}...")
    print(color.ENDC)
    result: SearchItemPaged[dict] = client.search(
        search_text=full_search_query,
        include_total_count=True,
        highlight_fields="ReviewText",
        search_mode="all",
        query_type="full",
        scoring_statistics="global")

    print(f"results number: {result.get_count()}")
    print_search_result(result)


# does not go to an analyzer
def proximity_search(client: SearchClient):
    query = f'ReviewText: "long adhesion"~7'
    print(f"Applied search with the query {color.OKCYAN} {query} {color.ENDC}...")
    print(color.ENDC)
    result: SearchItemPaged[dict] = client.search(
        search_text=query,
        include_total_count=True,
        highlight_fields="ReviewText",
        search_mode="all",
        query_type="full"
    )
    print(f"results number: {result.get_count()}")
    print_search_result(result)


# does not go to an analyzer
def entire_phrase_occurrence(client: SearchClient, text: str):
    query = f'ReviewText: "{text}"'
    print(f"Applied search with the query {color.OKCYAN} {query} {color.ENDC}...")
    print(color.ENDC)
    result: SearchItemPaged[dict] = client.search(
        search_text=query,
        include_total_count=True,
        highlight_fields="ReviewText",
        search_mode="all",
        query_type="full")
    print(f"results number: {result.get_count()}")
    print_search_result(result)


def filter_by_field(client: SearchClient, filter: str, query: str):
    print(
        f"Applied search with the query {color.OKCYAN} {query} {color.ENDC} and filter {color.OKCYAN} {filter} {color.ENDC}...")

    print(color.ENDC)

    result: SearchItemPaged[dict] = client.search(
        search_text=query,
        include_total_count=True,
        highlight_fields="ReviewText",
        search_mode="all",
        query_type="full",
        filter=filter)

    print(f"results number: {result.get_count()}")

    print_search_result(result)

    pass


if __name__ == "__main__":
    client: SearchClient = get_search_client("fowlart_product_review_hybrid")

    # entire_phrase_occurrence(client,"library cards and lunch")

    # proximity_search(client)
    # all_terms_are_present(client, ["picture"])

    # with proximity search
    # all_terms_are_present(client, ["saving", "pitcures~", "buy"])

    # with term boosting
    # all_terms_are_present(client, ["good", "product^2"])

    # with regexp and term boosting
    # all_terms_are_present(client, ["cards", "/[wear|tear]/","tear^3"])

    # filter_by_field(client=client, filter="ReviewRating eq 3", query="*")

    semantic_search(client, "ultrasound pictures and sonogram keeping")
