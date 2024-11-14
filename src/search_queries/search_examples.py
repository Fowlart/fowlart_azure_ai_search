from dataclasses import fields

from azure.search.documents import SearchClient, SearchItemPaged
from src.utils.common_utils import get_search_client
from src.utils.common_utils import bcolors as color

def print_search_result(iterator):
    for x in iterator:
        print(color.OKCYAN)
        print(x)
        print(color.ENDC)

#goes to analyzer
def all_terms_are_present(client: SearchClient,
                          terms: list[str]):
    search_prefix = "ReviewText:"
    modified_terms =[search_prefix+s for s in terms]
    full_search_query = " AND ".join(modified_terms)
    print(f"Applied search with the query {color.OKCYAN} {full_search_query} {color.ENDC}...")
    print(color.ENDC)
    result: SearchItemPaged[dict] = client.search(
        search_text=full_search_query,
        include_total_count=True,
        highlight_fields="ReviewText",
        search_mode="all",
        query_type="full"
    )
    print(f"results number: {result.get_count()}")
    print_search_result(result)

#does not go to an analyzer
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


#does not go to an analyzer 
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

    print(f"Applied search with the query {color.OKCYAN} {query} and filter {filter} {color.ENDC}...")

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

    # all_terms_are_present(client, ["saving","pictures","buy"])

    # with proximity search
    # all_terms_are_present(client, ["saving", "pitcures~", "buy"])

    # with term boosting
    # all_terms_are_present(client, ["good", "product^2"])

    # with regexp and term boosting
    #all_terms_are_present(client, ["cards", "/[wear|tear]/","tear^3"])

    filter_by_field(client=client, filter="ReviewRating eq 3", query="*")
