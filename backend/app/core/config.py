from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """
    This class reads all values from your .env file automatically.
    
    Your .env file has:
        POSTGRES_USER=postgres
        POSTGRES_PASSWORD=izone_password
        POSTGRES_DB=izone_db
        POSTGRES_HOST=postgres
        POSTGRES_PORT=5432
        SECRET_KEY=your-super-secret-key
    
    This class picks them up and makes them available as:
        settings.POSTGRES_USER
        settings.SECRET_KEY
        settings.database_url  ← built from the above values
    """

    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str
    POSTGRES_HOST: str
    POSTGRES_PORT: int = 5432
    SECRET_KEY: str

    @property
    def database_url(self) -> str:
        """
        Builds the full PostgreSQL connection string.
        Example result:
        postgresql://postgres:izone_password@localhost:5432/izone_db
        """
        return (
            f"postgresql://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}"
            f"@{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"
        )

    class Config:
        env_file = ".env"
        extra = "ignore"


# This creates ONE settings object used everywhere in the app.
# Other files just do: from app.core.config import settings
settings = Settings()
