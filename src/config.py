from pydantic import BaseSettings


class Config(BaseSettings):
    REDIS_DATABASE_ACCESS: int = 13
    PSQL_USER: str = "psql_user"
    PSQL_PASS: str = "psql_password"
    PSQL_HOST: str = "localhost"
    PSQL_PORT: int = 5436
    PSQL_DB: str = "psql_db"
    SECRET_KEY: str = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
    ENCODING_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    def get_psql_url(self) -> str:
        """
        Get URL to Postgres from internal options.

        Returns:
            Url to Postgres.
        """

        return (
            f"postgresql://{self.PSQL_USER}:{self.PSQL_PASS}@"
            f"{self.PSQL_HOST}:{self.PSQL_PORT}/{self.PSQL_DB}"
        )


CONFIG: Config = Config()
