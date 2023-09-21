from pydantic import BaseModel, Extra


class Config(BaseModel, extra=Extra.ignore):
    anti_insult_ban_time: int = 720
