from subprocess import Popen, PIPE
from typing import List, Optional, Tuple
import platform
from dotenv import load_dotenv
import os
from azure.search.documents.indexes import SearchIndexerClient
from azure.search.documents.indexes._search_index_client import SearchClient, SearchIndexClient
from azure.search.documents.indexes._generated.models import (CorsOptions,
                                                              ScoringProfile,
                                                              StopwordsTokenFilter,
                                                              PatternReplaceCharFilter,
                                                              SearchSuggester)
from azure.search.documents.indexes.models import (
    SemanticSearch,
    VectorSearch,
    SearchableField,
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

# Todo: refactor
# [Local env: BEGIN]
def get_iaac_folder_name() -> str:
    platform_name = str(platform.system()).lower()
    return "iaac_linux_bash" if "linux" in platform_name else "iaac_windows_powershell"

def get_correct_file_ext() -> str:
    folder_name = get_iaac_folder_name()
    return ".sh" if folder_name =="iaac_linux_bash" else ".ps1"

def get_terminal_command(file_name_to_execute: str) -> list[str]:
    folder_name = get_iaac_folder_name()
    win_cmd = ['powershell.exe', '-ExecutionPolicy', 'Bypass', '-File', f'..\\{folder_name}\\{file_name_to_execute}{get_correct_file_ext()}']
    linux_cmd = ['sh', f'../{get_iaac_folder_name()}/{file_name_to_execute}{get_correct_file_ext()}']
    return linux_cmd if "linux" in folder_name else win_cmd

def get_path_to_audio_sample() -> str:
    load_dotenv()
    return os.getenv("PATH_TO_SOUND_SAMPLE")

def get_path_to_gensim_model() -> str:
    load_dotenv()
    return os.getenv("PATH_TO_GENSIM_MODEL")

def get_path_to_example_data() -> str:
    load_dotenv()
    return os.getenv("PATH_TO_DELTA_TABLE")

def get_html_template_folder_path() -> str:
    platform_name = str(platform.system()).lower()
    return "../../resources/static-html/AzSearch.html" if "linux" in platform_name else "..\\..\\resources\\static-html\\AzSearch.html"

def get_test_index_name()->str:
    return "fowlart-product-review-hybrid"

def get_ai_search_endpoint() -> str:
    return f"https://fowlart-ai-search.search.windows.net"

def get_language_service_endpoint() -> str:
    return "https://fowlart-language-service.cognitiveservices.azure.com"

def _get_speech_service_key()->str:
    result = ""
    file_name = "speech_service_api_key"
    cmd = get_terminal_command(file_name)
    proc = Popen(cmd, stdout=PIPE, stderr=PIPE)
    print(f"{bcolors.OKBLUE} Starting speech service key extraction {bcolors.ENDC}")
    while True:
        line = proc.stdout.readline()
        if line != b'':
            the_line = line.decode("utf-8").strip()
            if "key is>" in the_line:
                result = the_line.split(">")[-1]
        else:
            break
    return result

def _get_language_service_key()->str:
    result = ""
    file_name = "language_service_api_key"
    cmd = get_terminal_command(file_name)
    proc = Popen(cmd, stdout=PIPE, stderr=PIPE)
    print(f"{bcolors.OKBLUE} Starting language service key extraction {bcolors.ENDC}")
    while True:
        line = proc.stdout.readline()
        if line != b'':
            print(line)
            the_line = line.decode("utf-8").strip()
            print(the_line)
            if "key is>" in the_line:
                result = the_line.split(">")[-1]
        else:
            break
    print(f"extracted-key: {result}")
    return result

def _get_search_service_key()->str:
    result = ""
    file_name = "ai_service_api_key"
    cmd = get_terminal_command(file_name)
    proc = Popen(cmd, stdout=PIPE, stderr=PIPE)
    print(f"{bcolors.OKBLUE} Starting search service key extraction {bcolors.ENDC}")
    while True:
        line = proc.stdout.readline()
        if line != b'':
            the_line = line.decode("utf-8").strip()
            if "key is>" in the_line:
                result = the_line.split(">")[-1]
        else:
            break
    return result

def _get_storage_account_connection_string()->str:
    result = ""
    file_name = "get_storage_account_connection_string"
    cmd = get_terminal_command(file_name)
    proc = Popen(cmd, stdout=PIPE, stderr=PIPE)
    print(f"{bcolors.OKBLUE} Starting {__name__}.{_get_search_service_key.__name__} {bcolors.ENDC}")
    while True:
        line = proc.stdout.readline()
        if line != b'':
            the_line = line.decode("utf-8").strip()
            if "connectionString is>" in the_line:
                result = the_line.split(">")[-1]
        else:
            break
    return result
# [Local env: END]

def get_search_indexer_client()-> SearchIndexerClient:
    service_endpoint = get_ai_search_endpoint()
    key = _get_search_service_key()
    return SearchIndexerClient(service_endpoint, AzureKeyCredential(key))


def get_search_index_client() -> SearchIndexClient:
    service_endpoint = get_ai_search_endpoint()
    key = _get_search_service_key()
    return SearchIndexClient(service_endpoint, AzureKeyCredential(key))


def get_search_client(index_name: str = None) -> SearchClient:
    service_endpoint = get_ai_search_endpoint()
    key = _get_search_service_key()
    index_name = get_test_index_name() if (index_name is None) else index_name

    return SearchClient(endpoint=service_endpoint,
                        credential=AzureKeyCredential(key),
                        index_name=index_name)

def get_text_analytics_client():
    ta_credential = AzureKeyCredential(_get_language_service_key())
    text_analytics_client = TextAnalyticsClient(
        endpoint=get_language_service_endpoint(),
        credential=ta_credential)
    return text_analytics_client

def get_query_key() -> str:
    result = ""
    file_name = "query_key"
    cmd = get_terminal_command(file_name)
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

def create_an_index(
        index_name: str,
        fields_definition: List[SearchableField],
        analyzers: Optional[List[LexicalAnalyzer]] = None,
        tokenizer: Optional[List[LexicalTokenizer]] = None,
        t_filter: Optional[List[TokenFilter]] = None,
        ch_filters: Optional[List[CharFilter]] = None,
        semantic_search: Optional[SemanticSearch] = None,
        vector_search: Optional[VectorSearch] = None,
        suggesters: Optional[list[SearchSuggester]] = None
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
                        fields_definition ="",
                        suggesters=suggesters)

    result: SearchIndex = search_index_client.create_or_update_index(index)

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

def extract_key_phrases(text: str,
                        client: TextAnalyticsClient,
                        language: str = None
                        ) -> list[str]:
    result = []
    try:
        documents = [text]
        response = client.extract_key_phrases(documents=documents,language = language)[0]
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