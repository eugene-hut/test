from fastapi import UploadFile
from pydantic import BaseModel, ConfigDict, field_validator


class Excel(BaseModel):
    file: UploadFile

    model_config = ConfigDict(
        str_strip_whitespace=True,
        from_attributes=True,
    )


class ReplacePhoto(Excel):
    text: str

    @field_validator("text", mode="after")
    def get_clear_text(cls, text: str):
        if not text.startswith(";"):
            text = ";" + text
        if text.endswith(";"):
            text = text.removesuffix(";")
        return text


class Duplicate(Excel):
    quantity: int
