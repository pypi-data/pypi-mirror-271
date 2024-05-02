import os
from enum import Enum

from deepgram import (
    DeepgramClient,
    DeepgramClientOptions,
    FileSource,
    PrerecordedOptions,
)
from dotenv import load_dotenv
from pydub import AudioSegment

load_dotenv()


class TRANSCRIPTION_TYPE(str, Enum):
    DEEPGRAM = "DEEPGRAM"


class Transcription:
    def __init__(self, type: TRANSCRIPTION_TYPE = TRANSCRIPTION_TYPE.DEEPGRAM):
        self.type = type
        self.client = self._create_client()

    def _create_client(self):
        api_key = os.getenv("DEEPGRAM_API_KEY")
        config = DeepgramClientOptions()
        return DeepgramClient(api_key, config)

    def invoke(self, audio_path: str):
        temp_audio_file = "temp.wav"
        self._convert_audio(audio_path, temp_audio_file)

        try:
            with open(temp_audio_file, "rb") as file:
                buffer_data = file.read()

            payload: FileSource = {"buffer": buffer_data}
            options = self._get_transcription_options()

            response = self.client.listen.prerecorded.v("1").transcribe_file(
                payload, options
            )
            transcript = response["results"]["channels"][0]["alternatives"][0][
                "paragraphs"
            ]["transcript"]

            return transcript
        except Exception as e:
            print(f"Exception: {e}")
        finally:
            os.remove(temp_audio_file)

    def _convert_audio(self, audio_path, output_path):
        audio = AudioSegment.from_file(audio_path)
        audio.export(output_path, format="wav")

    def _get_transcription_options(self):
        return PrerecordedOptions(
            model="nova-2",
            smart_format=True,
            utterances=True,
            punctuate=True,
            diarize=True,
            language="ja",
            filler_words=True,
        )
