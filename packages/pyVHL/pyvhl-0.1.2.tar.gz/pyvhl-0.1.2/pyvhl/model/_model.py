from pydantic import BaseModel, HttpUrl, validator


class StreamableVideo(BaseModel):
    shortcode: str
    url: HttpUrl = None

    @validator("url", pre=True, always=True)
    def url_validator(cls, v, values, **kwargs):
        return f"https://streamable.com/{values['shortcode']}"


class CatboxVideo(BaseModel):
    shortcode: str
    url: HttpUrl = None

    @validator("url", pre=True, always=True)
    def url_validator(cls, v, values, **kwargs):
        return f"https://files.catbox.moe/{values['shortcode']}"
