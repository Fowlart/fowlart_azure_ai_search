from azure.ai.textanalytics.aio import TextAnalyticsClient
from src.utils.common_utils import authenticate_text_analytics_client


def key_phrase_extraction(text: str, client: TextAnalyticsClient) -> list[str]:

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



if __name__ == "__main__":

   result = key_phrase_extraction("Key phrase extraction works best when you give it bigger amounts of text to work on. This is opposite from sentiment analysis, which performs better on smaller amounts of text. "
                                  "To get the best results from both operations, consider restructuring the inputs accordingly.",authenticate_text_analytics_client())

   print(result)