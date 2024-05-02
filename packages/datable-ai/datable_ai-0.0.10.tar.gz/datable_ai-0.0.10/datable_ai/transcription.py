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
    """
    Enum representing the types of transcription services.
    """

    DEEPGRAM = "DEEPGRAM"


class Transcription:
    """
    Class for performing audio transcription using various services.
    """

    def __init__(self, type: TRANSCRIPTION_TYPE = TRANSCRIPTION_TYPE.DEEPGRAM):
        """
        Initialize the Transcription class.

        Args:
            type (TRANSCRIPTION_TYPE): The type of transcription service to use. Defaults to DEEPGRAM.
        """
        self.type = type
        self.client = self._create_client()

    def _create_client(self):
        """
        Create a client for the selected transcription service.

        Returns:
            The created client object.
        """
        api_key = os.getenv("DEEPGRAM_API_KEY")
        config = DeepgramClientOptions()
        return DeepgramClient(api_key, config)

    def invoke(self, audio_path: str):
        """
        Invoke the transcription process on the given audio file.

        Args:
            audio_path (str): The path to the audio file.

        Returns:
            The transcribed text.
        """
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
        """
        Convert the audio file to the required format.

        Args:
            audio_path (str): The path to the input audio file.
            output_path (str): The path to save the converted audio file.
        """
        audio = AudioSegment.from_file(audio_path)
        audio.export(output_path, format="wav")

    def _get_transcription_options(self):
        """
        Get the transcription options for the selected service.

        Returns:
            The transcription options.
        """
        return PrerecordedOptions(
            model="nova-2",
            smart_format=True,
            utterances=True,
            punctuate=True,
            diarize=True,
            language="ja",
            filler_words=True,
        )
