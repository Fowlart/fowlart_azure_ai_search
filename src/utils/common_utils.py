from operator import index
from subprocess import Popen, PIPE
from typing import List, Optional, Tuple
from azure.search.documents.indexes._search_index_client import SearchClient, SearchIndexClient
from azure.search.documents.indexes._generated.models import SearchFieldDataType, CorsOptions, ScoringProfile, \
    StopwordsTokenFilter, PatternReplaceCharFilter
from azure.search.documents.indexes.models import (
    SemanticSearch,
    SimpleField,
    VectorSearch,
    SearchableField,
    ComplexField,
    SearchIndex,
    LexicalAnalyzer,
    LexicalTokenizer,
    TokenFilter,
    CharFilter,
    AnalyzeTextOptions, PatternTokenizer, CustomAnalyzer)
from azure.ai.textanalytics import TextAnalyticsClient
from azure.core.credentials import AzureKeyCredential

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def _get_index_name()->str:
    return "fowlart_product_review_hybrid"

def _get_language_service_key()->str:
    result = ""
    cmd = ['powershell.exe', '-ExecutionPolicy', 'Bypass', '-File', '..\\iaac_powershell\\language_service_api_key.ps1']
    proc = Popen(cmd, stdout=PIPE, stderr=PIPE)
    print(f"{bcolors.OKBLUE} Starting {__name__}.{_get_language_service_key.__name__} {bcolors.ENDC}")
    while True:
        line = proc.stdout.readline()
        if line != b'':
            the_line = line.decode("utf-8").strip()
            if "key is>" in the_line:
                result = the_line.split(">")[-1]
        else:
            break
    return result


def _get_search_service_key()->str:
    result = ""
    cmd = ['powershell.exe', '-ExecutionPolicy', 'Bypass', '-File', '..\\iaac_powershell\\ai_service_api_key.ps1']
    proc = Popen(cmd, stdout=PIPE, stderr=PIPE)
    print(f"{bcolors.OKBLUE} Starting {__name__}.{_get_search_service_key.__name__} {bcolors.ENDC}")
    while True:
        line = proc.stdout.readline()
        if line != b'':
            the_line = line.decode("utf-8").strip()
            if "key is>" in the_line:
                result = the_line.split(">")[-1]
        else:
            break
    return result


def get_search_index_client() -> SearchIndexClient:
    service_endpoint = "https://fowlart-ai-search.search.windows.net"
    key = _get_search_service_key()
    return SearchIndexClient(service_endpoint, AzureKeyCredential(key))


def get_search_client() -> SearchClient:
    service_endpoint = "https://fowlart-ai-search.search.windows.net"

    key = _get_search_service_key()

    return SearchClient(endpoint=service_endpoint,
                                          credential=AzureKeyCredential(key),
                                          index_name=_get_index_name())

def get_text_analytics_client():
    ta_credential = AzureKeyCredential(_get_language_service_key())
    text_analytics_client = TextAnalyticsClient(
        endpoint=r"https://fowlart-language-service.cognitiveservices.azure.com/",
        credential=ta_credential)
    return text_analytics_client


def create_an_index(
        index_name: str,
        fields_definition: List[SearchableField],
        analyzers: Optional[List[LexicalAnalyzer]] = None,
        tokenizer: Optional[List[LexicalTokenizer]] = None,
        t_filter: Optional[List[TokenFilter]] = None,
        ch_filters: Optional[List[CharFilter]] = None,
        semantic_search: Optional[SemanticSearch] = None,
        vector_search: Optional[VectorSearch] = None
) -> SearchIndex:

    search_index_client: SearchIndexClient = get_search_index_client()


    cors_options = CorsOptions(allowed_origins=["*"], max_age_in_seconds=60)

    scoring_profiles: List[ScoringProfile] = []

    index = SearchIndex(name=index_name,
                        fields=fields_definition,
                        scoring_profiles=scoring_profiles,
                        cors_options=cors_options,
                        analyzers=analyzers,
                        tokenizers=tokenizer,
                        token_filters=t_filter,
                        char_filters=ch_filters,
                        semantic_search=semantic_search,
                        vector_search=vector_search,
                        fields_definition =""
                        )

    result: SearchIndex = search_index_client.create_index(index)

    if isinstance(result, SearchIndex):
        print(f"{bcolors.OKGREEN} Index with name {result.name} was created {bcolors.ENDC}")

    return result

def get_tokens(text:str, analyzer_name: str, index_name: str, client: SearchIndexClient) -> list[str]:
    op: AnalyzeTextOptions = AnalyzeTextOptions(text=text,analyzer_name=analyzer_name)
    resp: dict[str] = client.analyze_text(index_name, op).as_dict()
    return [str(el["token"]) for el in resp.get("tokens")]


def analyze_text(text:str, analyzer_name: str, index_name: str):

    client: SearchIndexClient = get_search_index_client()

    print(f"{bcolors.OKGREEN} text: {text} \n {bcolors.OKCYAN}analyzer: {analyzer_name} {bcolors.ENDC}")

    op: AnalyzeTextOptions = AnalyzeTextOptions(text=text,analyzer_name=analyzer_name)

    resp: dict[str] = client.analyze_text(index_name, op).as_dict()

    for _elem in resp.get("tokens"):
        print(_elem)

    pass

def extract_key_phrases(text: str, client: TextAnalyticsClient) -> list[str]:

    result = []

    try:
        documents = [text]

        response = client.extract_key_phrases(documents=documents)[0]

        if not response.is_error:
            result = response.key_phrases
        else:
            print(response.id, response.error)

    except Exception as err:
        print("Encountered exception. {}".format(err))

    return result

def get_custom_analyzer() -> Tuple[PatternTokenizer,StopwordsTokenFilter,PatternReplaceCharFilter,CustomAnalyzer]:

    pattern_tokenizer = PatternTokenizer(pattern=r"\W+", name="my_pattern_tokenizer")

    token_filter = StopwordsTokenFilter(name="my_token_filter", stopwords=["Dog", "Cat", "Pig"], ignore_case=True)

    char_filter = PatternReplaceCharFilter(name="my_char_filter", pattern=r"=n=", replacement="<new_line>")

    my_custom_analyzer = CustomAnalyzer(name="my_custom_analyzer",
                                        tokenizer_name="my_pattern_tokenizer",
                                        token_filters=["my_token_filter"],
                                        char_filters=["my_char_filter"])

    return pattern_tokenizer,token_filter,char_filter, my_custom_analyzer