from pydantic_settings  import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    GROQ_API_KEY: str 
    MONGO_URI: str 
    MONGO_DB: str 
    SECRET_KEY: str 
    ALGORITHM: str 
    ACCESS_TOKEN_EXPIRE_MINUTES: int

    model_config= SettingsConfigDict(env_file=".env.prod", env_file_encoding="utf-8")

config = Settings()

    
