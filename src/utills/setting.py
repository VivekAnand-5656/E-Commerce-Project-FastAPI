from pydantic_settings import BaseSettings, SettingsConfigDict
from dotenv import load_dotenv
import os
load_dotenv()

class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")
    DB_CONNECTION : str
    SECRET_KEY : str
    ALGORITHM : str
    EXP_TIME : int

setting = Settings()
print(setting.DB_CONNECTION)