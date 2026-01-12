import logging
import time
from typing import BinaryIO
import requests
from openai import OpenAI

logger = logging.getLogger(__name__)


class ATSClient:
    def __init__(self, url: str):
        self.ats_url = url 

    def speech_to_text(
        self, audio_file: BinaryIO, file_extension: str | None = None
    ) -> str:
        # A file extension is needed for cases where audio_file does not have a
        # name, such as when using in-memory files. The OpenAI SDK needs a name
        # to infer the file type, so we pass in a dummy file name.
        file: BinaryIO | tuple[str, BinaryIO]
        if file_extension is not None:
            file = (f"dummy.{file_extension}", audio_file)
        else:
            file = audio_file
        start_time = time.time()

        files = {"file": file}
			  response = requests.post(
				  self.ats_url,
				  files=files,
				  timeout=10
			  )
        
        logger.info(f"Time taken to transcribe: {time.time() - start_time:.2f}s")
        logger.info(f"Transcription: {result}")
        return result

    @property
    def model_name(self) -> str:
        return self._model
