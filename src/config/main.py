from pydantic.types import SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict


class SettingsBase(BaseSettings):
    model_config = SettingsConfigDict(env_file='.env', env_file_encoding='utf-8', extra='ignore')


class DBConfig(SettingsBase):
    model_config = SettingsConfigDict(env_prefix="db_")

    user: str
    password: SecretStr  # для вывода незашифрованного пароля нужно вызвать метод поля get_secret_value()
    host: str
    name: str

    def get_db_dsn(self):
        return f"postgresql+asyncpg://{self.user}:{self.password.get_secret_value()}@{self.host}/{self.name}"
        # return f"postgresql://{self.user}:{self.password.get_secret_value()}@{self.host}/{self.name}"
        # return "sqlite:///db/ua.db"


def db_config():
    return DBConfig()
