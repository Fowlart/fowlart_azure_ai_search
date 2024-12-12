import azure.cognitiveservices.speech as speechsdk
from utils.common_utils import _get_speech_service_key, get_path_to_audio_sample

def recognize_from_file():

    speech_config = speechsdk.SpeechConfig(subscription=_get_speech_service_key(),region="eastus2")

    speech_config.speech_recognition_language="uk-UA"

    audio_config = speechsdk.audio.AudioConfig(filename=get_path_to_audio_sample())

    speech_recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config, audio_config=audio_config)

    print("Starting...")

    # todo: async-await usage: recognize_once_async()
    speech_recognition_result = speech_recognizer.recognize_once()

    if speech_recognition_result.reason == speechsdk.ResultReason.RecognizedSpeech:
        print("Recognized: {}".format(speech_recognition_result.text))

    elif speech_recognition_result.reason == speechsdk.ResultReason.NoMatch:
        print("No speech could be recognized: {}".format(speech_recognition_result.no_match_details))

    elif speech_recognition_result.reason == speechsdk.ResultReason.Canceled:
        cancellation_details = speech_recognition_result.cancellation_details
        print("Speech Recognition canceled: {}".format(cancellation_details.reason))

        if cancellation_details.reason == speechsdk.CancellationReason.Error:
            print("Error details: {}".format(cancellation_details.error_details))
            print("Did you set the speech resource key and region values?")


if __name__ == "__main__":

    recognize_from_file()