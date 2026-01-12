import logging
import time
from typing import BinaryIO
import requests
import json

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
        result = parse_ats_response(response)
        
        logger.info(f"Time taken to transcribe: {time.time() - start_time:.2f}s")
        logger.info(f"Transcription: {result}")
        return result

    @property
    def model_name(self) -> str:
        return self._model

    def parse_ats_response(text: str) -> str:
    """Parse ATS response which may be:
       * a JSON array of objects
       * concatenated JSON objects without delimiters
       * newline‑delimited JSON objects.
    Returns the combined transcript string."""
    transcripts = []
    # Try to parse as JSON array first
    try:
        data = json.loads(text)
        if isinstance(data, list):
            for obj in data:
                if isinstance(obj, dict) and "transcript" in obj:
                    transcripts.append(str(obj["transcript"]))
            return " ".join(transcripts).strip()
    except json.JSONDecodeError:
        pass

    # Fallback: parse concatenated or newline‑delimited JSON objects
    idx = 0
    decoder = json.JSONDecoder()
    while idx < len(text):
        while idx < len(text) and text[idx].isspace():
            idx += 1
        if idx >= len(text):
            break
        try:
            obj, end = decoder.raw_decode(text[idx:])
            idx += end
            if isinstance(obj, dict) and "transcript" in obj:
                transcripts.append(str(obj["transcript"]))
        except json.JSONDecodeError as e:
            print(f"JSON parsing error at position {idx}: {e}")
            break
    return " ".join(transcripts).strip()
