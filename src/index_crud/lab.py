from typing import List
from azure.search.documents._generated.models import IndexingResult
from azure.search.documents.indexes._search_index_client import SearchClient
from azure.search.documents.indexes._generated.models import SearchFieldDataType
from azure.search.documents.indexes.models import SimpleField, SearchableField, ComplexField
from src.utils.common_utils import create_an_index, get_search_client


def add_the_documents_to_index(the_client: SearchClient) -> List[IndexingResult]:

    documents: list[dict] = [{
        "address": [{"streetAddress": "Kozelnycjka", "city": "Lviv"}],
        "hotelId": "1000",
        "baseRate": 4.0,
        "description": ["___description___"]}]

    print(documents)

    result = the_client.upload_documents(documents)

    print("Upload of new document succeeded: {}".format(result[0].succeeded))

    return result


if __name__ == "__main__":

     index_name = "fowlart_index"

     complex_field_definition = ComplexField(
         name="address",
         fields=[
             SimpleField(name="streetAddress", type=SearchFieldDataType.String),
             SimpleField(name="city", type=SearchFieldDataType.String),
         ], collection=True)

     fields: List[SearchableField] = [
         complex_field_definition,
         SimpleField(name="hotelId", type=SearchFieldDataType.String, key=True),
         SimpleField(name="baseRate", type=SearchFieldDataType.Double),
         SearchableField(name="description", type=SearchFieldDataType.String, collection=True),
     ]

     # create an index
     try:
        created_index = create_an_index(index_name, fields)

        print(f"The index with the name {created_index.name} was created!")
     except Exception as ex:
         print(repr(ex))

     client: SearchClient = get_search_client(index_name)

     # add documents to an index
     the_results: List[IndexingResult] = add_the_documents_to_index(client)

     print("IndexingResult")

     for index_res in the_results:
         print(index_res)

     # get documents from index
     the_document = client.get_document("1000")
     print(f"Extracted document: {the_document}")

     # document count
     print(f"Count of documents: {client.get_document_count()}")

     # dummy search
     search_results = client.search(search_text = "*")

     print("Find all: ")
     for x in search_results:
         print(x)