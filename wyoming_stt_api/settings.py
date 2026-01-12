from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    #url for private text to speech service
    ats_url: str
    
    
    server_host: str = "0.0.0.0"
    server_port: int = 10300

    max_audio_duration_s: int = 10
