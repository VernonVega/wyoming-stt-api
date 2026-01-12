import asyncio
import logging

from wyoming.server import AsyncTcpServer

from wyoming_stt_api.clients.ats import ATSClient
from wyoming_stt_api.services.wyoming import WyomingEventHandler
from wyoming_stt_api.settings import Settings

logging.basicConfig(
    level=logging.INFO, format="%(levelname)s %(name)s %(asctime)s %(message)s"
)

settings = Settings()
ats_client = ATSClient(
    ats_url=settings.ats_url
)
server = AsyncTcpServer(settings.server_host, settings.server_port)


def create_handler(reader: asyncio.StreamReader, writer: asyncio.StreamWriter):
    return WyomingEventHandler(
        ats_client, settings.max_audio_duration_s, reader, writer
    )
